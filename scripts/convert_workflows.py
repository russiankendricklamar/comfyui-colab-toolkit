#!/usr/bin/env python3
"""
Конвертер воркфлоу ComfyUI: saved формат -> API формат
Saved формат: nodes[] + links[] (как сохраняет UI)
API формат: {node_id: {class_type, inputs}} (как принимает /api/prompt)
"""

import json
import sys
import argparse
from pathlib import Path


# Маппинг widgets_values -> API inputs для каждого типа ноды.
# None в списке означает "пропустить этот виджет" (UI-only поля, напр. control_after_generate).
# None вместо списка означает "пропустить всю ноду" (display-only).
WIDGET_MAPPINGS = {
    # === Video — Wan (KiJai wrapper) ===
    "LoadWanVideoT5TextEncoder": ["model_name", "dtype", "offload_to", "lowvram"],
    "WanVideoModelLoader": [
        "model_name", "dtype", "quant_type", "offload_to", "attention_mode", "scheduler",
    ],
    "WanVideoVAELoader": ["model_name", "dtype"],
    "WanVideoBlockSwap": [
        "blocks_to_swap", "offload_img_enc", "offload_clipmodel", "offload_txt_enc",
        "double_blocks_to_swap", "single_blocks_to_swap", "offload_all",
    ],
    "WanVideoTextEncode": ["positive", "negative", "force_offload", "use_cache", "encode_on"],
    "WanVideoEmptyEmbeds": ["width", "height", "num_frames"],
    "WanVideoContextOptions": [
        "context_mode", "context_length", "context_overlap", "context_stride",
        "freenoise", "start_from_ref", "pyramid_mode",
    ],
    "WanVideoSampler": [
        "steps", "cfg", "shift", "seed", "force_offload", "scheduler",
        "start_step", "denoise_strength", "force_denoise", "noise_type",
        "skip_layer_start", "skip_layer_end", "pag_adaptive",
    ],
    "WanVideoDecode": [
        "enable_tiling", "tile_size_h", "tile_size_w",
        "tile_stride_h", "tile_stride_w", "decode_mode",
    ],
    "VHS_VideoCombine": None,

    # === Video — HunyuanVideo ===
    "DownloadAndLoadHunyuanVideo": [
        "model", "precision", "fp8_fastmode", "load_device", "attention_mode",
    ],
    "HunyuanVideoSampler": [
        "width", "height", "num_frames", "steps", "embedded_guidance_scale",
        "flow_shift", "seed", "force_offload", "denoise_strength",
    ],
    "HunyuanVideoTextEncode": ["prompt"],
    "HunyuanVideoVAEDecode": ["enable_tiling", "temporal_tiling"],

    # === Video — CogVideo ===
    "DownloadAndLoadCogVideoModel": [
        "model", "precision", "fp8_fastmode", "load_device", "attention_mode", "compile",
    ],
    "CogVideoSampler": [
        "width", "height", "num_frames", "steps", "cfg", "seed",
        "scheduler", "denoise_strength",
    ],
    "CogVideoTextEncode": ["prompt", "negative_prompt", "force_offload"],
    "CogVideoXVAEDecode": ["enable_tiling"],

    # === Общие ComfyUI ноды ===
    "LoadImage": ["image", "upload"],
    "CheckpointLoaderSimple": ["ckpt_name"],
    "CLIPTextEncode": ["text"],
    # KSampler: widgets = [seed, control_after_generate, steps, cfg, sampler_name, scheduler, denoise]
    "KSampler": ["seed", None, "steps", "cfg", "sampler_name", "scheduler", "denoise"],
    "VAEDecode": [],
    "VAEEncode": [],
    "SaveImage": ["filename_prefix"],
    "EmptyLatentImage": ["width", "height", "batch_size"],
    "Note": None,

    # === Loader ноды ===
    "CLIPVisionLoader": ["clip_name"],
    "CLIPLoader": ["clip_name", "type", "device"],
    "VAELoader": ["vae_name"],
    "UNETLoader": ["unet_name", "weight_dtype"],
    "UpscaleModelLoader": ["model_name"],

    # === IPAdapter ноды ===
    "IPAdapterModelLoader": ["model_name"],
    "IPAdapterInsightFaceLoader": ["provider"],
    "IPAdapterAdvanced": [
        "weight", "weight_type", "combine_embeds", "start_at", "end_at", "embeds_scaling",
    ],
    "IPAdapterFaceID": [
        "weight", "weight_v2", "weight_type", "combine_embeds",
        "start_at", "end_at", "embeds_scaling",
    ],

    # === KJNodes ===
    "LoadImagesFromFolderKJ": [
        "folder_path", "width", "height", "resize_method", "batch_size",
        "start_index", "load_always",
    ],
    "ImageResizeKJv2": [
        "width", "height", "upscale_method", "keep_proportion",
        "pad_color", "crop_position", "divisible_by", "device",
    ],
    "WidgetToString": ["id", "widget_name", "return_all", "node_title", "allowed_float_decimals"],

    # === Sampler ноды (advanced) ===
    "BasicScheduler": ["scheduler", "steps", "denoise"],
    "KSamplerSelect": ["sampler_name"],
    # RandomNoise: widgets = [noise_seed, control_after_generate]
    "RandomNoise": ["noise_seed", None],
    "CFGGuider": ["cfg"],
    "SamplerCustomAdvanced": [],

    # === Switch/Utility ноды ===
    "ImageMaskSwitch": ["select"],
    "PrimitiveStringMultiline": ["value"],

    # === Wan 2.2 advanced (native ComfyUI + community) ===
    "wanBlockSwap": ["blocks_to_swap", "offload_img_emb", "offload_txt_emb", "use_non_blocking"],
    "WanVideoNAG": ["nag_scale", "nag_alpha", "nag_tau", "input_type"],
    "TorchCompileModelWanVideo": [
        "backend", "fullgraph", "mode", "dynamic",
        "dynamo_cache_size_limit", "compile_transformer_blocks_only",
    ],
    "PatchModelPatcherOrder": ["patch_order", "full_load"],

    # === mxToolkit (slider UI nodes) ===
    "mxSlider": ["Xi", "Xf", "isfloatX"],
    "mxSlider2D": ["Xi", "Xf", "Yi", "Yf", "isfloatX", "isfloatY"],

    # === Upscale ===
    # UltimateSDUpscale: widgets = [upscale_by, seed, control_after_generate, steps, ...]
    "UltimateSDUpscale": [
        "upscale_by", "seed", None, "steps", "cfg", "sampler_name", "scheduler",
        "denoise", "mode_type", "tile_width", "tile_height", "mask_blur", "tile_padding",
        "seam_fix_mode", "seam_fix_denoise", "seam_fix_width", "seam_fix_mask_blur",
        "seam_fix_padding", "force_uniform_tiles", "tiled_decode",
    ],

    # === Easy Use nodes ===
    "easy convertAnything": ["output_type"],
    "easy cleanGpuUsed": [],
    "easy clearCacheAll": [],

    # === pythongosssss ===
    "MathExpression|pysssss": ["expression"],

    # === Image Saver (alexopus) ===
    "Image Saver": [
        "filename", "path", "extension", "steps", "cfg", "modelname",
        "sampler_name", "scheduler_name", "positive", "negative", "seed_value",
        "width", "height", "lossless_webp", "quality_jpeg_or_webp", "optimize_png",
        "counter", "denoise", "clip_skip", "time_format", "save_workflow_as_json",
        "embed_workflow", "additional_hashes", "download_civitai_data",
        "easy_remix", "show_preview", "custom",
    ],

    # === rgthree (UI-only / display-only) ===
    "Image Comparer (rgthree)": None,
    "Fast Groups Bypasser (rgthree)": None,
    "Fast Groups Muter (rgthree)": None,
    # Power Lora Loader: сложная структура виджетов, обрабатывается отдельно
    "Power Lora Loader (rgthree)": None,
}


def _extract_power_lora(widgets):
    """Извлекает конфигурации LoRA из Power Lora Loader (rgthree) виджетов."""
    if not isinstance(widgets, list):
        return {}

    inputs = {}
    lora_idx = 1
    for item in widgets:
        if isinstance(item, dict) and "lora" in item and item.get("on"):
            inputs[f"lora_{lora_idx:02d}"] = {
                "on": item["on"],
                "lora": item["lora"],
                "strength": item.get("strength", 1.0),
                "strengthTwo": item.get("strengthTwo"),
            }
            lora_idx += 1
    return inputs


def convert_workflow(saved_json):
    """Конвертирует saved формат в API формат."""
    nodes = saved_json.get("nodes", [])
    links = saved_json.get("links", [])

    nodes = [n for n in nodes if n.get("type") != "Note"]

    link_map = {}
    for link in links:
        link_id, src_node, src_slot, dst_node, dst_slot, link_type = link[:6]
        link_map[link_id] = (src_node, src_slot)

    api = {}

    for node in nodes:
        node_id = str(node["id"])
        class_type = node["type"]
        node_inputs = {}

        # 1. Собираем входы от связей (links)
        for inp in node.get("inputs", []):
            link_id = inp.get("link")
            if link_id is not None and link_id in link_map:
                src_node, src_slot = link_map[link_id]
                node_inputs[inp["name"]] = [str(src_node), src_slot]

        # 2. Собираем входы от виджетов
        widgets = node.get("widgets_values")

        if class_type == "Power Lora Loader (rgthree)":
            # Специальная обработка: извлечение LoRA конфигов из сложной структуры
            node_inputs.update(_extract_power_lora(widgets))

        elif widgets is not None and class_type in WIDGET_MAPPINGS:
            mapping = WIDGET_MAPPINGS[class_type]
            if mapping is not None:
                for i, name in enumerate(mapping):
                    if name is None:
                        continue  # Пропуск UI-only виджетов (control_after_generate и т.п.)
                    if i < len(widgets) and name not in node_inputs:
                        node_inputs[name] = widgets[i]

        elif isinstance(widgets, dict):
            for k, v in widgets.items():
                if k not in ("videopreview",):
                    node_inputs[k] = v

        api[node_id] = {
            "class_type": class_type,
            "inputs": node_inputs,
        }

    return api


def main():
    parser = argparse.ArgumentParser(
        description="Конвертер воркфлоу ComfyUI -> API формат"
    )
    parser.add_argument(
        "--input-dir", default="workflows", help="Папка с исходными воркфлоу"
    )
    parser.add_argument(
        "--output-dir", default=None, help="Папка для API-формата (по умолчанию: та же)"
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir

    if not input_dir.exists():
        print(f"Папка не найдена: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0

    for json_file in sorted(input_dir.glob("*.json")):
        if json_file.stem.endswith("_api") or json_file.stem.endswith("_colab"):
            skipped += 1
            continue

        if json_file.stat().st_size == 0:
            print(f"[пропуск] {json_file.name} — пустой файл")
            skipped += 1
            continue

        try:
            with open(json_file, "r") as f:
                saved = json.load(f)

            if "nodes" not in saved or "links" not in saved:
                print(f"[пропуск] {json_file.name} — не saved формат")
                skipped += 1
                continue

            api = convert_workflow(saved)

            output_name = f"{json_file.stem}_api.json"
            output_path = output_dir / output_name

            with open(output_path, "w") as f:
                json.dump(api, f, indent=2, ensure_ascii=False)

            print(f"[OK] {json_file.name} -> {output_name} ({len(api)} нод)")
            converted += 1

        except Exception as e:
            print(f"[ОШИБКА] {json_file.name}: {e}")

    print(f"\nИтого: {converted} сконвертировано, {skipped} пропущено")
    print("\nВАЖНО: API-формат требует ручной верификации!")
    print("   Маппинг widgets_values -> inputs может быть неточным.")
    print("   Рекомендуется проверить через ComfyUI: Load -> Save (API Format)")


if __name__ == "__main__":
    main()
