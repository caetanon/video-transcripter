import whisper
import torch
from pathlib import Path


def get_device(use_gpu: bool) -> str:
    if not use_gpu:
        return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def get_available_device() -> str:
    """Returns the best available device for display purposes."""
    if torch.cuda.is_available():
        return f"cuda ({torch.cuda.get_device_name(0)})"
    if torch.backends.mps.is_available():
        return "mps (Apple Silicon)"
    return "cpu"


def transcribe(
    video_path: str,
    model_name: str,
    language: str,
    use_gpu: bool,
    status_callback=None,
) -> dict:
    device = get_device(use_gpu)

    if status_callback:
        status_callback(f"Carregando modelo '{model_name}' em {device}...")

    model = whisper.load_model(model_name, device=device)

    if status_callback:
        status_callback(f"Transcrevendo com modelo '{model_name}' em {device}...")

    lang = None if language == "auto" else language
    # fp16 only works well on CUDA; MPS and CPU use fp32
    fp16 = device == "cuda"

    result = model.transcribe(
        video_path,
        language=lang,
        verbose=False,
        fp16=fp16,
    )

    return result
