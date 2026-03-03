#!/bin/bash
set -e

# =============================================================================
# ComfyUI Setup Script для RunPod Pod
# Устанавливает ComfyUI + Wan Video + все зависимости
# =============================================================================

# --- Цвета для вывода ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; }
step()    { echo -e "${CYAN}[STEP]${NC} $1"; }

# --- Баннер ---
echo -e "${CYAN}"
echo "============================================="
echo "   ComfyUI + Wan Video 2.2 для RunPod"
echo "   github.com/russiankendricklamar/"
echo "          comfyui-colab-toolkit"
echo "============================================="
echo -e "${NC}"

# =============================================================================
# 1. Определение GPU и выбор профиля
# =============================================================================
step "Определяю GPU..."

GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "Unknown, 0 MiB")
GPU_NAME=$(echo "$GPU_INFO" | cut -d',' -f1 | xargs)
GPU_MEM_MIB=$(echo "$GPU_INFO" | cut -d',' -f2 | grep -oP '\d+' || echo "0")

info "GPU: $GPU_NAME ($GPU_MEM_MIB MiB)"

# Профили: blocks_to_swap, width, height, max_frames
case "$GPU_NAME" in
    *H100*)
        BLOCKS_TO_SWAP=0;  WIDTH=1280; HEIGHT=720; MAX_FRAMES=721
        ;;
    *A100*)
        BLOCKS_TO_SWAP=0;  WIDTH=1280; HEIGHT=720; MAX_FRAMES=721
        ;;
    *A40*)
        BLOCKS_TO_SWAP=0;  WIDTH=1280; HEIGHT=720; MAX_FRAMES=721
        ;;
    *4090*)
        BLOCKS_TO_SWAP=0;  WIDTH=1280; HEIGHT=720; MAX_FRAMES=721
        ;;
    *3090*)
        BLOCKS_TO_SWAP=5;  WIDTH=1024; HEIGHT=576; MAX_FRAMES=601
        ;;
    *L4*)
        BLOCKS_TO_SWAP=10; WIDTH=1024; HEIGHT=576; MAX_FRAMES=601
        ;;
    *T4*)
        BLOCKS_TO_SWAP=20; WIDTH=832;  HEIGHT=480; MAX_FRAMES=481
        ;;
    *)
        warn "Неизвестная GPU ($GPU_NAME), использую консервативный профиль (T4)"
        BLOCKS_TO_SWAP=20; WIDTH=832; HEIGHT=480; MAX_FRAMES=481
        ;;
esac

info "Профиль: ${WIDTH}x${HEIGHT}, max_frames=${MAX_FRAMES}, blocks_to_swap=${BLOCKS_TO_SWAP}"

# =============================================================================
# 2. Клонирование ComfyUI
# =============================================================================
step "Устанавливаю ComfyUI..."

if [ ! -d /workspace/ComfyUI ]; then
    git clone https://github.com/comfyanonymous/ComfyUI.git /workspace/ComfyUI
    info "ComfyUI склонирован"
else
    info "ComfyUI уже установлен, пропускаю"
fi

cd /workspace/ComfyUI
pip install "numpy<2.0" -q
pip install -r requirements.txt -q
info "Зависимости ComfyUI установлены"

# =============================================================================
# 3. Кастомные ноды
# =============================================================================
step "Устанавливаю кастомные ноды..."

NODES_DIR="/workspace/ComfyUI/custom_nodes"
cd "$NODES_DIR"

# Клонирование нод (идемпотентно)
test -d ComfyUI-WanVideoWrapper    || git clone https://github.com/kijai/ComfyUI-WanVideoWrapper.git
test -d ComfyUI-VideoHelperSuite   || git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git
test -d ComfyUI-KJNodes            || git clone https://github.com/kijai/ComfyUI-KJNodes.git
test -d ComfyUI-Frame-Interpolation || git clone https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git
test -d ComfyUI-Impact-Pack        || git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git

# Установка зависимостей для каждой ноды
for node_dir in ComfyUI-WanVideoWrapper ComfyUI-VideoHelperSuite ComfyUI-KJNodes ComfyUI-Frame-Interpolation ComfyUI-Impact-Pack; do
    if [ -f "$node_dir/requirements.txt" ]; then
        pip install "numpy<2.0" -r "$node_dir/requirements.txt" -q 2>/dev/null || \
            warn "Не удалось установить зависимости для $node_dir"
    fi
done

# Скрипт установки Impact Pack
python ComfyUI-Impact-Pack/install.py 2>/dev/null || true

info "Кастомные ноды установлены"

# =============================================================================
# 4. Загрузка моделей
# =============================================================================
step "Загружаю модели..."

MODELS_DIR="/workspace/ComfyUI/models"

# Создаю директории для моделей
mkdir -p "$MODELS_DIR/diffusion_models"
mkdir -p "$MODELS_DIR/text_encoders"
mkdir -p "$MODELS_DIR/vae"
mkdir -p "$MODELS_DIR/upscale_models"

# Функция для загрузки с проверкой
download_model() {
    local url="$1"
    local output="$2"

    if [ -f "$output" ] && [ "$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output" 2>/dev/null)" -gt 1024 ]; then
        info "$(basename "$output") уже загружен, пропускаю"
        return 0
    fi

    info "Загружаю $(basename "$output")..."
    wget -q --show-progress -O "$output" "$url"

    # Проверка размера (>1KB)
    local size
    size=$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output" 2>/dev/null)
    if [ "$size" -lt 1024 ]; then
        error "Файл $(basename "$output") слишком маленький ($size байт), загрузка не удалась"
        rm -f "$output"
        return 1
    fi

    info "$(basename "$output") загружен ($size байт)"
}

if [ -d "/runpod-volume/models" ]; then
    # --- Network Volume найден: создаём симлинки ---
    info "Network Volume найден - создаю симлинки..."

    for subdir in diffusion_models text_encoders vae upscale_models; do
        if [ -d "/runpod-volume/models/$subdir" ]; then
            for f in /runpod-volume/models/"$subdir"/*; do
                [ ! -e "$f" ] && continue
                target="$MODELS_DIR/$subdir/$(basename "$f")"
                if [ ! -e "$target" ]; then
                    ln -sf "$f" "$target"
                    info "Симлинк: $(basename "$f")"
                fi
            done
        fi
    done

    info "Симлинки из Network Volume созданы"
else
    # --- Загрузка моделей напрямую ---
    info "Network Volume не найден, загружаю модели..."

    # Диффузионные модели
    download_model \
        "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors" \
        "$MODELS_DIR/diffusion_models/Wan2_2-T2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors"

    download_model \
        "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_2_Fun_VACE_module_A14B_LOW_bf16.safetensors" \
        "$MODELS_DIR/diffusion_models/Wan2_2_Fun_VACE_module_A14B_LOW_bf16.safetensors"

    # Текстовый энкодер
    download_model \
        "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5_xxl_fp8_e4m3fn_scaled.safetensors" \
        "$MODELS_DIR/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors"

    # VAE
    download_model \
        "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/wan2.2_vae.safetensors" \
        "$MODELS_DIR/vae/wan2.2_vae.safetensors"

    # Апскейлер
    download_model \
        "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth" \
        "$MODELS_DIR/upscale_models/RealESRGAN_x4plus.pth"

    # RIFE загружается автоматически при первом использовании
    info "RIFE модель загрузится автоматически при первом запуске"
fi

# =============================================================================
# 5. Копирование воркфлоу
# =============================================================================
step "Копирую воркфлоу..."

WORKFLOWS_DIR="/workspace/ComfyUI/user/default/workflows"
mkdir -p "$WORKFLOWS_DIR"

# Определяем корень репозитория относительно этого скрипта
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

if [ -d "$REPO_DIR/workflows" ] && ls "$REPO_DIR"/workflows/*.json 1>/dev/null 2>&1; then
    cp "$REPO_DIR"/workflows/*.json "$WORKFLOWS_DIR/"
    WF_COUNT=$(ls "$WORKFLOWS_DIR"/*.json 2>/dev/null | wc -l)
    info "Скопировано воркфлоу: $WF_COUNT"
else
    warn "Воркфлоу не найдены в репозитории ($REPO_DIR/workflows/), скачайте вручную"
fi

# =============================================================================
# 6. Сохранение профиля GPU в файл (для воркфлоу)
# =============================================================================
step "Сохраняю GPU-профиль..."

cat > /workspace/gpu_profile.json <<EOF
{
    "gpu_name": "$GPU_NAME",
    "gpu_memory_mib": $GPU_MEM_MIB,
    "blocks_to_swap": $BLOCKS_TO_SWAP,
    "width": $WIDTH,
    "height": $HEIGHT,
    "max_frames": $MAX_FRAMES
}
EOF

info "Профиль сохранён в /workspace/gpu_profile.json"

# =============================================================================
# 7. Запуск ComfyUI
# =============================================================================
step "Запускаю ComfyUI..."

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 &
COMFY_PID=$!

# Ожидание запуска (макс. 120 секунд)
info "Жду запуска ComfyUI (до 120 сек)..."
WAIT_COUNT=0
MAX_WAIT=120

while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if curl -s http://localhost:8188 >/dev/null 2>&1; then
        break
    fi
    sleep 2
    WAIT_COUNT=$((WAIT_COUNT + 2))
done

if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
    error "ComfyUI не запустился за ${MAX_WAIT} секунд"
    error "Проверьте логи: tail -f /workspace/ComfyUI/comfyui.log"
    exit 1
fi

# =============================================================================
# 8. Готово!
# =============================================================================
POD_ID="${RUNPOD_POD_ID:-$(hostname)}"

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}   ComfyUI готов!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "  GPU:        ${CYAN}$GPU_NAME${NC}"
echo -e "  Разрешение: ${CYAN}${WIDTH}x${HEIGHT}${NC}"
echo -e "  Кадры:      ${CYAN}${MAX_FRAMES}${NC}"
echo -e "  Swap:       ${CYAN}${BLOCKS_TO_SWAP} блоков${NC}"
echo ""
echo -e "  URL: ${GREEN}https://${POD_ID}-8188.proxy.runpod.net${NC}"
echo ""
echo -e "  ${YELLOW}Совет: профиль GPU сохранён в /workspace/gpu_profile.json${NC}"
echo ""

# Держим процесс активным
wait $COMFY_PID
