from pathlib import Path


def _format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def export_txt(result: dict, output_path: str) -> None:
    """Export transcription as plain text."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["text"].strip())


def export_srt(result: dict, output_path: str) -> None:
    """Export transcription as SRT subtitle file with timestamps."""
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"], start=1):
            start = _format_timestamp(segment["start"])
            end = _format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
