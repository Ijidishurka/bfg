import json
import os
from typing import Any

SETTINGS_FILE = "settings.json"

default_settings = {
    "built": {},
    "custom": {}
}

settings = {}


def init_settings() -> None:
    global settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Ошибка загрузки настроек")
            settings = default_settings.copy()
    else:
        settings = default_settings.copy()

    for section in default_settings:
        if section not in settings or not isinstance(settings[section], dict):
            settings[section] = {}

    save_settings()


def save_settings() -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def update_setting(key: str, value: Any, custom: bool = False) -> None:
    section = "custom" if custom else "built"
    if section not in settings:
        settings[section] = {}
    settings[section][key] = value
    save_settings()


def get_setting(key: str, default: Any, custom: bool = False) -> Any:
    section = "custom" if custom else "built"
    if section not in settings:
        settings[section] = {}

    if key not in settings[section]:
        settings[section][key] = default
        save_settings()

    return settings[section][key]
