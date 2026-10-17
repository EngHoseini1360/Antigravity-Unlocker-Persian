"""
شناسایی و جستجوی خودکار نصب‌های Antigravity و فایل‌های اجرایی هدف در ویندوز
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from .settings_manager import load_settings


def get_standard_candidate_paths() -> List[Path]:
    """مسیرهای متداول و استاندارد نصب Antigravity در ویندوز، مک‌اواس و لینوکس"""
    candidates = []
    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA", "")
        program_files = os.environ.get("ProgramFiles", "")
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "")

        candidates.extend([
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
        ])
    elif sys.platform == "darwin":
        # مسیرهای استاندارد macOS (Intel و Apple Silicon M1/M2/M3/M4)
        home = Path.home()
        candidates.extend([
            Path("/Applications/Antigravity.app"),
            Path("/Applications/Antigravity IDE.app"),
            home / "Applications" / "Antigravity.app",
            home / "Applications" / "Antigravity IDE.app",
            home / "Library" / "Application Support" / "Antigravity",
            home / "Library" / "Application Support" / "Antigravity IDE",
            home / "Library" / "Application Support" / "Code" / "User",
            home / ".antigravity",
            home / ".local" / "bin",
            Path("/usr/local/bin"),
            Path("/opt/homebrew/bin"),
        ])
    else:
        # مسیرهای متداول توزیع‌های مختلف لینوکس (Ubuntu, Debian, Fedora, Arch, ...)
        home = Path.home()
        candidates.extend([
            home / ".local" / "share" / "Antigravity",
            home / ".local" / "share" / "antigravity",
            home / ".local" / "share" / "Antigravity IDE",
            home / ".local" / "share" / "antigravity-ide",
            home / ".config" / "Antigravity",
            home / ".config" / "Antigravity IDE",
            Path("/opt/Antigravity"),
            Path("/opt/antigravity"),
            Path("/opt/Antigravity IDE"),
            Path("/opt/antigravity-ide"),
            Path("/usr/lib/antigravity"),
            Path("/usr/share/antigravity"),
            home / ".local" / "share" / "agy",
            home / ".local" / "bin",
            Path("/usr/local/bin"),
            home / ".antigravity",
        ])
    return candidates


def is_valid_install_root(path: Path) -> bool:
    """بررسی اینکه آیا مسیر داده شده یک پوشه معتبر نصب Antigravity است (ویندوز، مک، لینوکس)"""
    if not path.exists() or not path.is_dir():
        return False

    path_str = str(path).lower()
    if "c:\\windows" in path_str or "/proc" in path_str or "/sys" in path_str:
        return False

    # بررسی پکیج .app مکینتاش
    contents = path / "Contents"
    if contents.exists() and contents.is_dir():
        if (contents / "Resources").exists() or (contents / "MacOS").exists():
            return True

    resources = path / "resources"
    if resources.exists() and resources.is_dir():
        if (resources / "app.asar").exists() or (resources / "app").exists() or (resources / "bin").exists():
            return True

    for agy_name in ["agy.exe", "agy"]:
        if (path / agy_name).is_file():
            return True

    for bin_name in ["Antigravity.exe", "Antigravity IDE.exe", "antigravity.exe", "Antigravity", "antigravity", "antigravity-ide"]:
        if (path / bin_name).is_file():
            return True

    return False


def get_binary_targets_for_install(install_root: Path) -> List[Path]:
    """یافتن تمام فایل‌های اجرایی باینری Language Server و CLI در پوشه نصب (ویندوز، مک، لینوکس)"""
    targets = []
    
    # پوشه پایه منابع (برای مک‌اواس در Contents قرار دارد)
    base_dirs = [install_root]
    if (install_root / "Contents").is_dir():
        base_dirs.append(install_root / "Contents")

    for base in base_dirs:
        # 1. agy executable
        for agy_name in ["agy.exe", "agy"]:
            agy_bin = base / agy_name
            if agy_bin.is_file() and agy_bin not in targets:
                targets.append(agy_bin)

        # 2. Desktop language server
        res_bin_dir = base / "resources" / "bin" if (base / "resources").is_dir() else base / "Resources" / "bin"
        if res_bin_dir.is_dir():
            for filename in [
                "language_server.exe", "language_server",
                "language_server_darwin_arm64", "language_server_darwin_x64",
                "language_server_linux_x64", "language_server_windows_x64.exe"
            ]:
                candidate = res_bin_dir / filename
                if candidate.is_file() and candidate not in targets:
                    targets.append(candidate)
            try:
                for item in res_bin_dir.glob("language_server*"):
                    if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")) and item not in targets:
                        targets.append(item)
            except Exception:
                pass

        # 3. IDE language server
        ide_res = base / "resources" if (base / "resources").is_dir() else base / "Resources"
        ide_bin_dir = ide_res / "app" / "extensions" / "antigravity" / "bin"
        if ide_bin_dir.is_dir():
            for filename in [
                "language_server_darwin_arm64", "language_server_darwin_x64",
                "language_server_windows_x64.exe", "language_server.exe",
                "language_server_linux_x64", "language_server"
            ]:
                candidate = ide_bin_dir / filename
                if candidate.is_file() and candidate not in targets:
                    targets.append(candidate)
            try:
                for item in ide_bin_dir.glob("language_server*"):
                    if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")) and item not in targets:
                        targets.append(item)
            except Exception:
                pass

        # 4. MacOS binary directory
        macos_bin_dir = base / "MacOS"
        if macos_bin_dir.is_dir():
            for filename in ["Antigravity", "Antigravity IDE", "agy"]:
                candidate = macos_bin_dir / filename
                if candidate.is_file() and candidate not in targets:
                    targets.append(candidate)

    return targets


def identify_install_label(install_root: Path) -> str:
    """تعیین نام و عنوان مناسب برای برنامه نصب شده"""
    name_lower = install_root.name.lower()
    if "ide" in name_lower or (install_root / "Antigravity IDE.exe").is_file() or (install_root / "antigravity-ide").is_file():
        return "محیط توسعه Antigravity IDE"
    elif "agy" in name_lower or (install_root / "agy.exe").is_file() or (install_root / "agy").is_file():
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
