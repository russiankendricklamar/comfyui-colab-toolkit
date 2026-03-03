# ============================================================
# Stage 1: Base — ComfyUI + кастомные ноды + зависимости
# ============================================================
FROM nvidia/cuda:12.6.3-cudnn-runtime-ubuntu24.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Системные зависимости: Python 3.12, git, ffmpeg, OpenGL для рендеринга
RUN apt-get update && apt-get install -y \
    python3.12 python3.12-venv python3-pip \
    git wget ffmpeg libgl1 libglib2.0-0 \
    && ln -sf /usr/bin/python3.12 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# Клонируем ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /comfyui
WORKDIR /comfyui

# Устанавливаем зависимости ComfyUI с ограничением numpy<2.0
# (numpy 2.x ломает совместимость с некоторыми нодами)
RUN echo "numpy<2.0" > /tmp/numpy_constraint.txt && \
    pip install "numpy>=1.26,<2.0" && \
    pip install -r requirements.txt -c /tmp/numpy_constraint.txt

# Кастомные ноды для генерации видео
WORKDIR /comfyui/custom_nodes
RUN git clone https://github.com/kijai/ComfyUI-WanVideoWrapper.git && \
    git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git && \
    git clone https://github.com/kijai/ComfyUI-KJNodes.git && \
    git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git && \
    git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git

# Установка зависимостей каждой ноды (|| true — чтобы сборка не падала
# из-за опциональных пакетов)
RUN for dir in */; do \
        if [ -f "$dir/requirements.txt" ]; then \
            pip install -r "$dir/requirements.txt" -c /tmp/numpy_constraint.txt || true; \
        fi; \
    done && \
    python ComfyUI-Impact-Pack/install.py 2>/dev/null || true

# Копируем файлы serverless-воркера
COPY handler.py /handler.py
COPY start.sh /start.sh
COPY extra_model_paths.yaml /comfyui/extra_model_paths.yaml
RUN chmod +x /start.sh

# RunPod SDK и зависимости handler
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Воркфлоу в API-формате (prompt-ready JSON)
# Скопируйте *_api.json файлы в директорию сборки перед docker build:
#   cp ../../workflows/*_api.json ./workflows/
COPY workflows/ /workflows/

WORKDIR /comfyui

# ============================================================
# Stage 2: Model downloader — скачивание моделей (кешируется Docker layer cache)
# Каждая модель в отдельном RUN — при изменении одной не перекачиваются остальные
# ============================================================
FROM base AS downloader

RUN mkdir -p /models/diffusion_models /models/text_encoders /models/vae /models/upscale_models

# Wan2.2 T2V — основная модель генерации видео (~7GB, fp8 квантизация)
RUN wget -q --show-progress -O /models/diffusion_models/Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors"

# Wan2.2 Fun VACE — модуль для V2V/inpainting (~7GB)
RUN wget -q --show-progress -O /models/diffusion_models/Wan2_2_Fun_VACE_module_A14B_LOW_bf16.safetensors \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_2_Fun_VACE_module_A14B_LOW_bf16.safetensors"

# UMT5-XXL — текстовый энкодер для промптов (~5GB, fp8)
RUN wget -q --show-progress -O /models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5_xxl_fp8_e4m3fn_scaled.safetensors"

# VAE — декодер латентов в пиксели (~300MB)
RUN wget -q --show-progress -O /models/vae/wan2.2_vae.safetensors \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/wan2.2_vae.safetensors"

# RealESRGAN x4 — апскейлер для пост-обработки (~64MB)
RUN wget -q --show-progress -O /models/upscale_models/RealESRGAN_x4plus.pth \
    "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"

# ============================================================
# Stage 3: Final — объединение base + модели
# ============================================================
FROM base AS final

# === Вариант 1: wan-full (~25GB образ) ===
# Модели запечены в образ — cold start ~30 сек, не нужен Network Volume
COPY --from=downloader /models/diffusion_models/ /comfyui/models/diffusion_models/
COPY --from=downloader /models/text_encoders/ /comfyui/models/text_encoders/
COPY --from=downloader /models/vae/ /comfyui/models/vae/
COPY --from=downloader /models/upscale_models/ /comfyui/models/upscale_models/

# === Вариант 2: base (~5GB образ) ===
# Закомментируйте COPY выше — модели берутся с Network Volume
# через extra_model_paths.yaml (см. start.sh для авто-детекта)

CMD ["/start.sh"]
