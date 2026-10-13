from functools import cache
from pathlib import Path
import yaml


@cache
def load(language: str) -> dict[str, str]:
    return yaml.safe_load(Path(__file__).with_name(f"{language}.yml").read_text(encoding="utf-8"))


def translate(key: str, language: str | None = None) -> str:
    language = (language or "en").lower().replace("_", "-").split("-")[0]
    if language not in ("en", "ru"):
        language = "en"
    if key in load(language):
        return load(language)[key]
    return load("en")[key]