#!/bin/bash
set -e

echo "=== Запуск ComfyUI Serverless Worker ==="

# Оптимизация CUDA — expandable_segments уменьшает фрагментацию VRAM
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# Если есть Network Volume с моделями — подключаем через extra_model_paths
if [ -d "/runpod-volume/models" ]; then
    echo "Network Volume найден — используем модели с тома"
    export COMFYUI_EXTRA_MODEL_PATHS="/comfyui/extra_model_paths.yaml"
fi

# Запуск ComfyUI в фоне (слушает только localhost — безопасность)
echo "Запуск ComfyUI..."
cd /comfyui
python -u main.py --disable-auto-launch --disable-metadata --listen 127.0.0.1 --port 8188 &

# Ожидание готовности ComfyUI (макс 60 сек)
echo "Ожидание готовности ComfyUI..."
for i in $(seq 1 60); do
    if curl -s http://127.0.0.1:8188/api/system_stats > /dev/null 2>&1; then
        echo "ComfyUI готов за ${i} сек!"
        break
    fi
    sleep 1
done

# Запуск RunPod handler — принимает задачи из очереди RunPod
echo "Запуск RunPod handler..."
python -u /handler.py
