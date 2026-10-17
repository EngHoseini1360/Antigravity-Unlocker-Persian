"""
شناسایی و جستجوی خودکار نصب‌های Antigravity و فایل‌های اجرایی هدف در ویندوز
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from .settings_manager import load_settings


def get_standard_candidate_paths() -> List[Path]:
    """مسیرهای متداول و استاندارد نصب Antigravity در ویندوز"""
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    program_files = os.environ.get("ProgramFiles", "")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", "")

    candidates = [
        Path(local_appdata) / "Programs" / "Antigravity",
        Path(local_appdata) / "Programs" / "Antigravity IDE",
        Path(program_files) / "Antigravity",
        Path(program_files) / "Antigravity IDE",
        Path(program_files_x86) / "Antigravity",
        Path(program_files_x86) / "Antigravity IDE",
        Path(local_appdata) / "Antigravity",
        Path(local_appdata) / "Antigravity IDE",
        Path(local_appdata) / "agy" / "bin",
        Path(local_appdata) / "agy",
    ]
    return candidates


def is_valid_install_root(path: Path) -> bool:
    """بررسی اینکه آیا مسیر داده شده یک پوشه معتبر نصب Antigravity است"""
    if not path.exists() or not path.is_dir():
        return False

    path_str = str(path).lower()
    if "c:\\windows" in path_str:
        return False

    resources = path / "resources"
    if resources.exists() and resources.is_dir():
        if (resources / "app.asar").exists() or (resources / "app").exists() or (resources / "bin").exists():
            return True

    if (path / "agy.exe").is_file():
        return True

    if (path / "Antigravity.exe").is_file() or (path / "Antigravity IDE.exe").is_file() or (path / "antigravity.exe").is_file():
        return True

    return False


def get_binary_targets_for_install(install_root: Path) -> List[Path]:
    """یافتن تمام فایل‌های اجرایی باینری Language Server و CLI در پوشه نصب"""
    targets = []
    
    # 1. agy.exe
    agy_exe = install_root / "agy.exe"
    if agy_exe.is_file():
        targets.append(agy_exe)

    # 2. Desktop language server
    desktop_bin = install_root / "resources" / "bin" / "language_server.exe"
    if desktop_bin.is_file():
        targets.append(desktop_bin)

    # 3. IDE language server
    ide_bin_dir = install_root / "resources" / "app" / "extensions" / "antigravity" / "bin"
    if ide_bin_dir.is_dir():
        for filename in ["language_server_windows_x64.exe", "language_server.exe"]:
            candidate = ide_bin_dir / filename
            if candidate.is_file() and candidate not in targets:
                targets.append(candidate)
        # Any other language_server*.exe in ext bin dir
        try:
            for item in ide_bin_dir.glob("language_server*.exe"):
                if item.is_file() and not item.name.endswith(".agtmp") and item not in targets:
                    targets.append(item)
        except Exception:
            pass

    # 4. Any other language_server*.exe in resources\bin
    res_bin_dir = install_root / "resources" / "bin"
    if res_bin_dir.is_dir():
        try:
            for item in res_bin_dir.glob("language_server*.exe"):
                if item.is_file() and not item.name.endswith(".agtmp") and item not in targets:
                    targets.append(item)
        except Exception:
            pass

    return targets


def identify_install_label(install_root: Path) -> str:
    """تعیین نام و عنوان مناسب برای برنامه نصب شده"""
    name_lower = install_root.name.lower()
    if "ide" in name_lower or (install_root / "Antigravity IDE.exe").is_file():
        return "محیط توسعه Antigravity IDE"
    elif "agy" in name_lower or (install_root / "agy.exe").is_file():
        return "خط فرمان Antigravity CLI (agy)"
    else:
        return "نرم‌افزار دسکتاپ Antigravity 2.0"


def scan_all_installs() -> List[Dict]:
    """
    اسکن جامع تمام مسیرها برای شناسایی نصب‌های موجود در ویندوز.
    اطلاعات هر نصب شامل عنوان، مسیر، و لیست فایل‌های باینری قابل پچ است.
    """
    candidates = get_standard_candidate_paths()

    # خواندن مسیرهای دستی از تنظیمات
    settings = load_settings()
    manual_paths = settings.get("manual_paths", [])
    for mp in manual_paths:
        p = Path(mp)
        if p not in candidates:
            candidates.append(p)

    found_installs = []
    seen_roots = set()

    for cand in candidates:
        if not cand.exists():
            continue

        resolved_root: Optional[Path] = None
        if is_valid_install_root(cand):
            resolved_root = cand
        else:
            # بررسی زیرپوشه‌ها
            for sub in ["Programs\\Antigravity", "Programs\\Antigravity IDE", "Antigravity", "Antigravity IDE", "agy"]:
                check_sub = cand / sub
                if is_valid_install_root(check_sub):
                    resolved_root = check_sub
                    break

        if resolved_root and resolved_root not in seen_roots:
            seen_roots.add(resolved_root)
            binaries = get_binary_targets_for_install(resolved_root)
            label = identify_install_label(resolved_root)
            found_installs.append({
                "label": label,
                "path": str(resolved_root),
                "binaries": [str(b) for b in binaries]
            })

    return found_installs
