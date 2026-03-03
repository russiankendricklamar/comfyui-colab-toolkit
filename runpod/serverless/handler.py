"""
RunPod Serverless Handler для ComfyUI
Принимает workflow + параметры → запускает генерацию → возвращает результат
"""

import os
import json
import time
import base64
import uuid
import glob
import logging
import requests
import websocket
import runpod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("comfyui-handler")

COMFYUI_URL = "http://127.0.0.1:8188"
COMFYUI_OUTPUT = "/comfyui/output"
COMFYUI_INPUT = "/comfyui/input"
WORKFLOWS_DIR = "/workflows"
MAX_WAIT_SEC = 600  # 10 минут максимум на генерацию

# ==================== РЕЕСТР ВОРКФЛОУ ====================
WORKFLOW_REGISTRY = {
    "video_wan_t2v": "video_wan_t2v_api.json",
    "video_wan_clip": "video_wan_clip_api.json",
    "video_wan_v2v": "video_wan_v2v_api.json",
    "video_wan_talking": "video_wan_talking_api.json",
    "video_wan_long_ultimate": "video_wan_long_ultimate_api.json",
    "video_wan_reels": "video_wan_reels_api.json",
    "video_wan_dancer": "video_wan_dancer_api.json",
    "video_hunyuan_t2v": "video_hunyuan_t2v_api.json",
    "video_cogvideo_t2v": "video_cogvideo_t2v_api.json",
    "photo_flux_instagram": "photo_flux_instagram_api.json",
    "photo_flux_img2img": "photo_flux_img2img_api.json",
    "photo_wan_img2img": "photo_wan_img2img_api.json",
}


def wait_for_comfyui(timeout=120):
    """Ожидание готовности ComfyUI."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{COMFYUI_URL}/api/system_stats", timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def validate_input(job_input):
    """Валидация входных данных."""
    if not isinstance(job_input, dict):
        return "input должен быть объектом"

    workflow = job_input.get("workflow")
    if not workflow:
        return "workflow обязателен (имя из реестра или полный API JSON)"

    # Если workflow — строка, проверяем реестр
    if isinstance(workflow, str) and workflow not in WORKFLOW_REGISTRY:
        available = ", ".join(sorted(WORKFLOW_REGISTRY.keys()))
        return f"Неизвестный workflow: {workflow}. Доступные: {available}"

    return None


def resolve_workflow(workflow_input):
    """Загрузка workflow по имени или использование переданного JSON."""
    # Если передан полный API JSON (dict)
    if isinstance(workflow_input, dict):
        return workflow_input

    # Загрузка по имени из реестра
    filename = WORKFLOW_REGISTRY[workflow_input]
    filepath = os.path.join(WORKFLOWS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Workflow файл не найден: {filepath}")

    with open(filepath, "r") as f:
        return json.load(f)


def upload_media(media_list):
    """Загрузка base64 медиа в ComfyUI input/."""
    os.makedirs(COMFYUI_INPUT, exist_ok=True)
    uploaded = {}

    for item in media_list:
        name = item.get("name", f"{uuid.uuid4().hex[:8]}.jpg")
        data = base64.b64decode(item["image"])
        filepath = os.path.join(COMFYUI_INPUT, name)
        with open(filepath, "wb") as f:
            f.write(data)
        uploaded[name] = filepath
        logger.info(f"Загружен: {name} ({len(data)} байт)")

    return uploaded


def inject_params(workflow, job_input):
    """Подстановка параметров в workflow."""
    prompt_text = job_input.get("prompt")
    params = job_input.get("params", {})
    images = job_input.get("images", [])

    for node_id, node in workflow.items():
        if not isinstance(node, dict):
            continue
        inputs = node.get("inputs", {})
        class_type = node.get("class_type", "")

        # Инъекция текстового промпта
        if prompt_text:
            for key in ["text", "prompt", "positive"]:
                if key in inputs and isinstance(inputs[key], str):
                    inputs[key] = prompt_text

        # Инъекция разрешения и кадров
        if "width" in params and "width" in inputs:
            inputs["width"] = params["width"]
        if "height" in params and "height" in inputs:
            inputs["height"] = params["height"]
        if "num_frames" in params and "num_frames" in inputs:
            inputs["num_frames"] = params["num_frames"]

        # Инъекция параметров сэмплера
        if "steps" in params and "steps" in inputs:
            inputs["steps"] = params["steps"]
        if "cfg" in params and "cfg" in inputs:
            inputs["cfg"] = params["cfg"]
        if "seed" in params and "seed" in inputs:
            inputs["seed"] = params["seed"]

        # Инъекция изображения
        if images and class_type in ("LoadImage", "Load Image"):
            # Используем первое загруженное изображение
            inputs["image"] = images[0].get("name", "input.jpg")

    return workflow


def queue_prompt(workflow):
    """Отправка workflow в очередь ComfyUI."""
    resp = requests.post(
        f"{COMFYUI_URL}/prompt",
        json={"prompt": workflow},
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("prompt_id")


def wait_completion(prompt_id):
    """WebSocket мониторинг прогресса генерации."""
    ws_url = COMFYUI_URL.replace("http", "ws")
    ws = None

    try:
        ws = websocket.create_connection(
            f"{ws_url}/ws?clientId=runpod-handler",
            timeout=MAX_WAIT_SEC
        )

        start = time.time()
        while time.time() - start < MAX_WAIT_SEC:
            result = ws.recv()
            if not result:
                continue

            try:
                msg = json.loads(result)
            except json.JSONDecodeError:
                continue

            msg_type = msg.get("type")
            msg_data = msg.get("data", {})

            # Прогресс
            if msg_type == "progress":
                value = msg_data.get("value", 0)
                max_val = msg_data.get("max", 1)
                pct = int(value / max_val * 100) if max_val else 0
                logger.info(f"Прогресс: {pct}% ({value}/{max_val})")

            # Завершение
            if msg_type == "executing":
                if msg_data.get("node") is None and msg_data.get("prompt_id") == prompt_id:
                    logger.info("Генерация завершена!")
                    return True

            # Ошибка
            if msg_type == "execution_error":
                error = msg_data.get("exception_message", "Неизвестная ошибка")
                raise RuntimeError(f"ComfyUI ошибка: {error}")

    except websocket.WebSocketTimeoutException:
        raise TimeoutError(f"Таймаут генерации ({MAX_WAIT_SEC} сек)")
    finally:
        if ws:
            ws.close()

    return False


def wait_completion_polling(prompt_id):
    """Запасной вариант: polling /history вместо WebSocket."""
    start = time.time()
    while time.time() - start < MAX_WAIT_SEC:
        try:
            resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=15)
            history = resp.json()
            if prompt_id in history:
                return history[prompt_id]
        except Exception:
            pass
        time.sleep(3)
    raise TimeoutError(f"Таймаут генерации ({MAX_WAIT_SEC} сек)")


def collect_outputs(prompt_id):
    """Сбор результатов генерации из истории ComfyUI."""
    resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=15)
    history = resp.json()

    if prompt_id not in history:
        raise RuntimeError("Результат не найден в истории")

    outputs = []
    result = history[prompt_id]

    for node_id, node_output in result.get("outputs", {}).items():
        # ВАЖНО: собираем images, gifs И videos (official worker пропускает gifs/videos)
        for output_type in ("images", "gifs", "videos"):
            for item in node_output.get(output_type, []):
                filename = item.get("filename")
                subfolder = item.get("subfolder", "")
                if not filename:
                    continue

                filepath = os.path.join(COMFYUI_OUTPUT, subfolder, filename)
                if not os.path.exists(filepath):
                    continue

                # Кодирование в base64
                with open(filepath, "rb") as f:
                    data = base64.b64encode(f.read()).decode("utf-8")

                # Определение типа
                ext = os.path.splitext(filename)[1].lower()
                mime_map = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".mp4": "video/mp4",
                    ".webm": "video/webm",
                    ".webp": "image/webp",
                }

                outputs.append({
                    "filename": filename,
                    "type": output_type.rstrip("s"),  # images->image, videos->video
                    "mime": mime_map.get(ext, "application/octet-stream"),
                    "data": data,
                    "size": os.path.getsize(filepath),
                })

    return outputs


# ==================== ГЛАВНЫЙ HANDLER ====================

def handler(job):
    """Основной обработчик RunPod задач."""
    job_input = job.get("input", {})

    try:
        # 1. Валидация
        error = validate_input(job_input)
        if error:
            return {"error": error}

        # 2. Проверка готовности ComfyUI
        if not wait_for_comfyui(timeout=30):
            return {"error": "ComfyUI не отвечает"}

        # 3. Загрузка workflow
        workflow = resolve_workflow(job_input["workflow"])

        # 4. Загрузка медиа (если есть)
        if job_input.get("images"):
            upload_media(job_input["images"])

        # 5. Инъекция параметров
        workflow = inject_params(workflow, job_input)

        # 6. Отправка в очередь
        prompt_id = queue_prompt(workflow)
        if not prompt_id:
            return {"error": "Не удалось поставить в очередь"}
        logger.info(f"Prompt ID: {prompt_id}")

        # 7. Ожидание завершения (WebSocket с fallback на polling)
        try:
            wait_completion(prompt_id)
        except Exception as ws_err:
            logger.warning(f"WebSocket ошибка: {ws_err}, переключаюсь на polling")
            wait_completion_polling(prompt_id)

        # 8. Сбор результатов
        outputs = collect_outputs(prompt_id)

        if not outputs:
            return {"error": "Генерация завершена, но файлы не найдены"}

        return {
            "status": "success",
            "outputs": outputs,
            "prompt_id": prompt_id,
        }

    except TimeoutError as e:
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Handler ошибка: {e}", exc_info=True)
        return {"error": str(e)}


# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    logger.info("Запуск RunPod Serverless Handler...")
    logger.info(f"Доступные workflow: {list(WORKFLOW_REGISTRY.keys())}")
    runpod.serverless.start({"handler": handler})
