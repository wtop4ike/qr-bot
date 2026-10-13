from pathlib import Path
import pytest
import sys
sys.path.append(str(Path(__file__).parent.parent))
from translations import load, translate


def get_language_files() -> list[Path]:
    """Dynamically find all .yml files in the translations directory."""
    translations_dir = Path(__file__).parent.parent / "translations"
    return list(translations_dir.glob("*.yml"))


def test_loading_files():
    yml_files = get_language_files()
    assert len(yml_files) > 0, "No translation files (.yml) found in the translations directory."

    for file_path in yml_files:
        lang_code = file_path.stem
        data = load(lang_code)
        
        assert isinstance(data, dict), f"File {file_path.name} must contain a dictionary."
        assert len(data) > 0, f"Translation file {file_path.name} is empty."


def test_translate():
    yml_files = get_language_files()
    en_data = load("en")

    for file_path in yml_files:
        lang_code = file_path.stem
        lang_data = load(lang_code)
        for key, expected_value in lang_data.items():
            assert translate(key, language=lang_code) == expected_value
    if en_data:
        sample_key = next(iter(en_data))
        assert translate(sample_key, language="unknown_language") == en_data[sample_key]


def test_normalization():
    en_data = load("en")
    if not en_data:
        pytest.skip("English dictionary is empty, skipping edge case tests.")

    sample_key = next(iter(en_data))
    assert translate(sample_key) == en_data[sample_key]
    assert translate(sample_key, language=None) == en_data[sample_key]
    assert translate(sample_key, language="EN-us") == en_data[sample_key]
    yml_files = get_language_files()
    for file_path in yml_files:
        lang_code = file_path.stem
        lang_data = load(lang_code)
        if not lang_data:
            continue
        
        lang_key = next(iter(lang_data))
        expected_value = lang_data[lang_key]
        variants = [
            lang_code.upper(),
            f"{lang_code}_US",
            f"{lang_code.capitalize()}-123"
        ]
        
        for variant in variants:
            assert translate(lang_key, language=variant) == expected_value