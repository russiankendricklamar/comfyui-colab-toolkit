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


WIDGET_MAPPINGS = {
    "LoadWanVideoT5TextEncoder": ["model_name", "dtype", "offload_to", "lowvram"],
    "WanVideoModelLoader": ["model_name", "dtype", "quant_type", "offload_to", "attention_mode", "scheduler"],
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
    "LoadImage": ["image", "upload"],
    "Note": None,
    "LoadImagesFromFolderKJ": ["folder_path", "sort_by", "start_index", "max_images", "batch_size"],
    "CheckpointLoaderSimple": ["ckpt_name"],
    "CLIPTextEncode": ["text"],
    "KSampler": ["seed", "steps", "cfg", "sampler_name", "scheduler", "denoise"],
    "VAEDecode": [],
    "SaveImage": ["filename_prefix"],
    "EmptyLatentImage": ["width", "height", "batch_size"],
    "DownloadAndLoadHunyuanVideo": ["model", "precision", "fp8_fastmode", "load_device", "attention_mode"],
    "HunyuanVideoSampler": [
        "width", "height", "num_frames", "steps", "embedded_guidance_scale",
        "flow_shift", "seed", "force_offload", "denoise_strength",
    ],
    "HunyuanVideoTextEncode": ["prompt"],
    "HunyuanVideoVAEDecode": ["enable_tiling", "temporal_tiling"],
    "DownloadAndLoadCogVideoModel": [
        "model", "precision", "fp8_fastmode", "load_device", "attention_mode", "compile",
    ],
    "CogVideoSampler": [
        "width", "height", "num_frames", "steps", "cfg", "seed",
        "scheduler", "denoise_strength",
    ],
    "CogVideoTextEncode": ["prompt", "negative_prompt", "force_offload"],
    "CogVideoXVAEDecode": ["enable_tiling"],
}


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

        for inp in node.get("inputs", []):
            link_id = inp.get("link")
            if link_id is not None and link_id in link_map:
                src_node, src_slot = link_map[link_id]
                node_inputs[inp["name"]] = [str(src_node), src_slot]

        widgets = node.get("widgets_values")
        if widgets is not None and class_type in WIDGET_MAPPINGS:
            mapping = WIDGET_MAPPINGS[class_type]
            if mapping is not None:
                for i, name in enumerate(mapping):
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
