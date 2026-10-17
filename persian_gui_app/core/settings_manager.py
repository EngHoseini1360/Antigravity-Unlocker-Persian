"""
مدیریت تنظیمات و ذخیره‌سازی در settings.json واقع در %LOCALAPPDATA%\\AGUnlocker
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


def get_appdata_dir() -> Path:
    """دریافت مسیر پوشه داده‌های برنامه در LocalAppData"""
    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        local_appdata = os.path.expanduser("~\\AppData\\Local")
    path = Path(local_appdata) / "AGUnlocker"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_settings_file_path() -> Path:
    """دریافت مسیر فایل settings.json"""
    return get_appdata_dir() / "settings.json"


def get_gate_file_path() -> Path:
    """دریافت مسیر فایل وضعیت دروازه gate.json"""
    return get_appdata_dir() / "gate.json"


def get_forwarder_log_path() -> Path:
    """دریافت مسیر فایل لاگ رله forwarder.log"""
    return get_appdata_dir() / "forwarder.log"


def get_watchdog_log_path() -> Path:
    """دریافت مسیر فایل لاگ نگهبان watchdog.log"""
    return get_appdata_dir() / "watchdog.log"


def default_settings() -> Dict[str, Any]:
    """تنظیمات پیش‌فرض برنامه"""
    return {
        "client_patch": True,
        "auto_patch": True,
        "group_key": "",
        "license_key": "",
        "group_key_at": 0,
        "own_proxy_at": 0,
        "patch_declined": False,
        "dns": False,
        "local_proxy": False,
        "builtin_exits": True,
        "group_proxy": True,
        "disabled_providers": [],
        "rotate_providers": True,
        "provider_order": [],
        "vpn_detect": False,
        "verify_tls": True,
        "own_proxy": "127.0.0.1:10808",
        "own_proxy_enabled": True,
        "manual_paths": [],
    }


def load_settings() -> Dict[str, Any]:
    """خواندن تنظیمات ذخیره شده از فایل"""
    file_path = get_settings_file_path()
    defaults = default_settings()
    if not file_path.exists():
        return defaults

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            defaults.update(data)
            return defaults
    except Exception as e:
        print(f"خطا در خواندن فایل تنظیمات: {e}")
        return defaults


def save_settings(settings: Dict[str, Any]) -> bool:
    """ذخیره تنظیمات در فایل با فرمت خوانا"""
    file_path = get_settings_file_path()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"خطا در ذخیره فایل تنظیمات: {e}")
        return False


def update_setting(key: str, value: Any) -> bool:
    """بروزرسانی یک کلید خاص در تنظیمات"""
    current = load_settings()
    current[key] = value
    return save_settings(current)


def load_gate_status() -> Dict[str, Any]:
    """خواندن وضعیت دروازه و روت‌های شبکه از gate.json"""
    file_path = get_gate_file_path()
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}
