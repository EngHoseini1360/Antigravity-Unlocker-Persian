"""
شناسایی و جستجوی خودکار نصب‌های Antigravity و فایل‌های اجرایی هدف در ویندوز، لینوکس (دبیان، ترموکس و ...) و مک‌اواس
"""

import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional
from .settings_manager import load_settings


KNOWN_BINARY_NAMES = [
    "language_server",
    "language_server_linux_arm64",
    "language_server_linux_x64",
    "language_server_darwin_arm64",
    "language_server_darwin_x64",
    "language_server.exe",
    "language_server_windows_x64.exe",
    "language_server_windows_arm64.exe",
    "agy",
    "agy.exe",
]


def get_standard_candidate_paths() -> List[Path]:
    """مسیرهای متداول و استاندارد نصب Antigravity در ویندوز، مک‌اواس و لینوکس/ترموکس"""
    candidates = []

    # ۱. مسیر جاری اجرای برنامه و دایرکتوری‌های مجاور (بسیار متداول در ترموکس و لینوکس)
    try:
        cwd = Path.cwd()
        candidates.extend([cwd, cwd.parent])
    except Exception:
        pass

    # ۲. بررسی دستورات ثبت‌شده در متغیر محیطی PATH سیستم
    for cmd in ["antigravity", "antigravity-ide", "agy", "language_server"]:
        found_bin = shutil.which(cmd)
        if found_bin:
            try:
                p = Path(found_bin).resolve()
                candidates.extend([p, p.parent, p.parent.parent])
            except Exception:
                pass

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
        # مسیرهای متداول توزیع‌های مختلف لینوکس، دبیان، ترموکس (Termux / PRoot) و کانتینرها
        home = Path.home()
        candidates.extend([
            home,
            home / "antigravity",
            home / "Antigravity",
            home / "antigravity-ide",
            home / "Antigravity IDE",
            home / "antigravity-2.24.0",
            home / "Antigravity-2.24.0",
            home / "Downloads" / "antigravity",
            home / "Downloads" / "Antigravity",
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
            Path("/usr/local/antigravity"),
            home / ".local" / "share" / "agy",
            home / ".local" / "bin",
            home / "bin",
            Path("/usr/local/bin"),
            Path("/usr/bin"),
            home / ".antigravity",
            # ترموکس و اندروید (Termux & Android PRoot)
            Path("/data/data/com.termux/files/home"),
            Path("/data/data/com.termux/files/home/antigravity"),
            Path("/data/data/com.termux/files/usr/bin"),
            Path("/data/data/com.termux/files/usr/opt"),
            Path("/sdcard/antigravity"),
            Path("/sdcard/Download/antigravity"),
            Path("/storage/emulated/0/Download/antigravity"),
            Path("/storage/emulated/0/antigravity"),
            # افزونه‌های VS Code، code-server، VSCodium در لینوکس و ترموکس
            home / ".vscode" / "extensions",
            home / ".vscode-server" / "extensions",
            home / ".openvscode-server" / "extensions",
            home / ".vscode-oss" / "extensions",
            home / ".local" / "share" / "code-server" / "extensions",
            home / ".cursor" / "extensions",
            Path("/root/.vscode-server/extensions"),
            Path("/root/.vscode/extensions"),
        ])
    return candidates


def is_valid_install_root(path: Path) -> bool:
    """بررسی اینکه آیا مسیر داده شده یک پوشه معتبر یا فایل اجرایی Antigravity است"""
    if not path.exists():
        return False

    # اگر کاربر مستقیماً به یک فایل باینری اشاره کرده باشد
    if path.is_file():
        name_lower = path.name.lower()
        if "language_server" in name_lower or "agy" in name_lower or "antigravity" in name_lower:
            return True
        return False

    path_str = str(path).lower()
    if "c:\\windows" in path_str or "/proc" in path_str or "/sys" in path_str or "/dev" in path_str:
        return False

    # بررسی پکیج .app مکینتاش
    contents = path / "Contents"
    if contents.exists() and contents.is_dir():
        if (contents / "Resources").exists() or (contents / "MacOS").exists():
            return True

    # بررسی ساختار باینری‌های استاندارد در داخل پوشه یا پوشه bin
    for b_name in KNOWN_BINARY_NAMES:
        if (path / b_name).is_file():
            return True
        if (path / "bin" / b_name).is_file():
            return True

    # بررسی ساختار منابع Electron
    resources = path / "resources"
    if resources.exists() and resources.is_dir():
        if (resources / "app.asar").exists() or (resources / "app").exists() or (resources / "bin").exists():
            return True

    # بررسی فایل‌های اجرایی لانچر
    for bin_name in ["Antigravity.exe", "Antigravity IDE.exe", "antigravity.exe", "Antigravity", "antigravity", "antigravity-ide"]:
        if (path / bin_name).is_file():
            return True

    # جستجوی سریع تا ۱ سطح عمق برای یافتن هر فایل با پیشوند language_server
    try:
        for item in path.glob("language_server*"):
            if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")):
                return True
        if (path / "bin").is_dir():
            for item in (path / "bin").glob("language_server*"):
                if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")):
                    return True
    except Exception:
        pass

    return False


def get_binary_targets_for_install(install_root: Path) -> List[Path]:
    """یافتن تمام فایل‌های اجرایی باینری Language Server و CLI در مسیر مشخص شده"""
    targets = []

    # ۱. اگر مسیر یک فایل باینری مستقیم باشد
    if install_root.is_file():
        name_lower = install_root.name.lower()
        if not install_root.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")):
            if "language_server" in name_lower or "agy" in name_lower:
                return [install_root]
        return targets

    # ۲. جستجو در پوشه ریشه و زیرپوشه bin
    check_subdirs = [install_root, install_root / "bin"]
    if (install_root / "Contents").is_dir():
        check_subdirs.extend([
            install_root / "Contents",
            install_root / "Contents" / "Resources" / "bin",
            install_root / "Contents" / "MacOS"
        ])
    if (install_root / "resources" / "bin").is_dir():
        check_subdirs.append(install_root / "resources" / "bin")
    if (install_root / "resources" / "app" / "extensions" / "antigravity" / "bin").is_dir():
        check_subdirs.append(install_root / "resources" / "app" / "extensions" / "antigravity" / "bin")
    if (install_root / "extensions" / "antigravity" / "bin").is_dir():
        check_subdirs.append(install_root / "extensions" / "antigravity" / "bin")

    for sdir in check_subdirs:
        if not sdir.is_dir():
            continue
        for b_name in KNOWN_BINARY_NAMES:
            cand = sdir / b_name
            if cand.is_file() and cand not in targets:
                targets.append(cand)
        try:
            for item in sdir.glob("language_server*"):
                if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")) and item not in targets:
                    targets.append(item)
        except Exception:
            pass

    # ۳. در صورتی که هنوز فایلی پیدا نشده، یک جستجوی عمیق‌تر تا ۳ سطح انجام می‌دهیم
    if not targets:
        try:
            for item in install_root.rglob("language_server*"):
                if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")):
                    # جلوگیری از رفتن به عمق زیاد یا پوشه‌های کش
                    parts = item.relative_to(install_root).parts
                    if len(parts) <= 5 and ".git" not in parts and "__pycache__" not in parts:
                        if item not in targets:
                            targets.append(item)
            for item in install_root.rglob("agy*"):
                if item.is_file() and not item.name.endswith((".agtmp", ".bak", ".old", ".txt", ".log")):
                    parts = item.relative_to(install_root).parts
                    if len(parts) <= 5 and ".git" not in parts and "__pycache__" not in parts:
                        if item not in targets:
                            targets.append(item)
        except Exception:
            pass

    return targets


def identify_install_label(install_root: Path) -> str:
    """تعیین نام و عنوان مناسب برای برنامه یا باینری پیدا شده"""
    if install_root.is_file():
        return f"فایل باینری مستقیم ({install_root.name})"

    name_lower = install_root.name.lower()
    path_lower = str(install_root).lower()

    if "ide" in name_lower or (install_root / "Antigravity IDE.exe").is_file() or (install_root / "antigravity-ide").is_file():
        return "محیط توسعه Antigravity IDE"
    elif "extensions" in path_lower and "antigravity" in path_lower:
        return "افزونه Antigravity در ویرایشگر کد (VS Code / Cursor)"
    elif "agy" in name_lower or (install_root / "agy.exe").is_file() or (install_root / "agy").is_file():
        return "خط فرمان Antigravity CLI (agy)"
    else:
        return "نرم‌افزار دسکتاپ Antigravity"


def scan_all_installs() -> List[Dict]:
    """
    اسکن جامع تمام مسیرها برای شناسایی نصب‌های موجود در ویندوز، لینوکس و مک.
    اطلاعات هر نصب شامل عنوان، مسیر، و لیست فایل‌های باینری قابل پچ است.
    """
    candidates = get_standard_candidate_paths()

    # خواندن مسیرهای دستی از تنظیمات
    settings = load_settings()
    manual_paths = settings.get("manual_paths", [])
    for mp in manual_paths:
        try:
            p = Path(mp)
            if p not in candidates:
                candidates.append(p)
        except Exception:
            pass

    found_installs = []
    seen_roots = set()

    # زیرپوشه‌های متداول
    sub_folder_names = [
        Path("Programs") / "Antigravity",
        Path("Programs") / "Antigravity IDE",
        Path("Antigravity"),
        Path("Antigravity IDE"),
        Path("antigravity"),
        Path("antigravity-ide"),
        Path("antigravity-2.24.0"),
        Path("Antigravity-2.24.0"),
        Path("agy"),
        Path("bin"),
    ]

    for cand in candidates:
        if not cand.exists():
            continue

        # اگر پوشه افزونه‌ها باشد (مثل .vscode/extensions)، داخل آن را برای پوشه antigravity بررسی کن
        if cand.is_dir() and "extensions" in cand.name.lower():
            try:
                for sub in cand.iterdir():
                    if sub.is_dir() and "antigravity" in sub.name.lower():
                        if is_valid_install_root(sub):
                            cand_res = sub.resolve()
                            if cand_res not in seen_roots:
                                seen_roots.add(cand_res)
                                binaries = get_binary_targets_for_install(sub)
                                if binaries:
                                    found_installs.append({
                                        "label": identify_install_label(sub),
                                        "path": str(sub),
                                        "binaries": [str(b) for b in binaries]
                                    })
            except Exception:
                pass

        resolved_root: Optional[Path] = None
        if is_valid_install_root(cand):
            resolved_root = cand
        elif cand.is_dir():
            # بررسی زیرپوشه‌های رایج
            for sub in sub_folder_names:
                check_sub = cand / sub
                if is_valid_install_root(check_sub):
                    resolved_root = check_sub
                    break

        if resolved_root:
            try:
                res_key = resolved_root.resolve()
            except Exception:
                res_key = resolved_root

            if res_key not in seen_roots:
                seen_roots.add(res_key)
                binaries = get_binary_targets_for_install(resolved_root)
                if binaries:
                    label = identify_install_label(resolved_root)
                    found_installs.append({
                        "label": label,
                        "path": str(resolved_root),
                        "binaries": [str(b) for b in binaries]
                    })

    return found_installs
