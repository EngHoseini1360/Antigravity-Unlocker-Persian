"""
منطق پچ، آنپچ و بازرسی باینری‌های Antigravity به صورت ایمن و Atomic
جایگزینی دقیق بایت‌ها بدون تغییر اندازه و بدون دستکاری ساختار PE فایل اجرایی
"""

import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple

# امضاهای پچ باینری (طول بایت‌ها دقیقا باید یکسان باشد)
SIG_FIELD_UNPATCHED = b"ineligible"      # طول: ۱۰ بایت
SIG_FIELD_PATCHED   = b"inexigible"      # طول: ۱۰ بایت

SIG_PROXY_UNPATCHED = b"https_proxy"     # طول: ۱۱ بایت
SIG_PROXY_PATCHED   = b"AG_LS_PROXY"     # طول: ۱۱ بایت


def kill_holding_processes(file_name: str = "") -> None:
    """بستن فرآیندهایی که ممکن است فایل اجرایی را قفل کرده باشند (ویندوز یا لینوکس)"""
    procs_to_kill = [
        "language_server.exe", "language_server_windows_x64.exe", "agy.exe",
        "language_server", "language_server_linux_x64", "agy"
    ]
    if file_name and file_name not in procs_to_kill:
        procs_to_kill.append(file_name)

    for proc in procs_to_kill:
        try:
            if sys.platform == "win32":
                kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}
                subprocess.run(
                    ["taskkill", "/F", "/IM", proc],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    **kwargs
                )
            else:
                subprocess.run(
                    ["pkill", "-9", "-f", proc],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except Exception:
            pass
    time.sleep(0.5)


_BINARY_STATUS_CACHE = {}


def check_binary_status(filepath: str, force: bool = False) -> Dict:
    """
    بررسی دقیق وضعیت پچ یک فایل اجرایی با قابلیت کشینگ هوشمند بر اساس زمان ویرایش و اندازه فایل
    """
    p = Path(filepath)
    if not p.exists() or not p.is_file():
        return {
            "status": "missing",
            "message": "فایل یافت نشد",
            "field_patched": 0,
            "field_unpatched": 0,
            "proxy_patched": 0,
            "proxy_unpatched": 0
        }

    try:
        f_stat = p.stat()
        cache_key = (str(p.resolve()), f_stat.st_mtime, f_stat.st_size)
        if not force and cache_key in _BINARY_STATUS_CACHE:
            return _BINARY_STATUS_CACHE[cache_key]

        with open(p, "rb") as f:
            data = f.read()


        c_inex = data.count(SIG_FIELD_PATCHED)
        c_inel = data.count(SIG_FIELD_UNPATCHED)
        c_ag_proxy = data.count(SIG_PROXY_PATCHED)
        c_https_proxy = data.count(SIG_PROXY_UNPATCHED)

        if c_inex > 0 and c_inel == 0:
            status = "patched"
            message = "پچ شده و آماده (تحریم رفع شده)"
        elif c_inel > 0 and c_inex == 0:
            status = "unpatched"
            message = "پچ نشده (محدود به ریجن)"
        elif c_inex > 0 and c_inel > 0:
            status = "partial"
            message = "پچ جزئی"
        else:
            status = "unknown"
            message = "امضای شناخته شده یافت نشد"

        res = {
            "status": status,
            "message": message,
            "field_patched": c_inex,
            "field_unpatched": c_inel,
            "proxy_patched": c_ag_proxy,
            "proxy_unpatched": c_https_proxy,
            "size_mb": round(len(data) / (1024 * 1024), 2)
        }
        _BINARY_STATUS_CACHE[cache_key] = res
        return res

    except PermissionError:
        return {
            "status": "locked",
            "message": "فایل توسط سیستم یا برنامه در حال اجرا قفل است",
            "field_patched": 0,
            "field_unpatched": 0,
            "proxy_patched": 0,
            "proxy_unpatched": 0
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"خطا در خواندن فایل: {e}",
            "field_patched": 0,
            "field_unpatched": 0,
            "proxy_patched": 0,
            "proxy_unpatched": 0
        }


def _safe_write_atomic(target_path: Path, data: bytes) -> Tuple[bool, str]:
    """نوشتن اتمیک برای جلوگیری از خراب شدن فایل اجرایی در صورت قطعی یا خطا"""
    tmp_path = target_path.with_name(f"{target_path.name}.{os.getpid()}.agtmp")
    try:
        with open(tmp_path, "wb") as f:
            f.write(data)
        
        # جایگزینی اتمیک
        try:
            os.replace(tmp_path, target_path)
            return True, "عملیات با موفقیت انجام شد."
        except PermissionError:
            # فایل احتمالا توسط پروسه در حال اجرا قفل است
            kill_holding_processes(target_path.name)
            time.sleep(0.6)
            os.replace(tmp_path, target_path)
            return True, "عملیات با موفقیت انجام شد."
    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        return False, str(e)


def patch_binary_file(filepath: str) -> Tuple[bool, str]:
    """
    پچ کردن یک فایل باینری خاص:
    تبدیل ineligible به inexigible و https_proxy به AG_LS_PROXY
    """
    p = Path(filepath)
    if not p.exists():
        return False, f"فایل وجود ندارد: {filepath}"

    try:
        with open(p, "rb") as f:
            data = bytearray(f.read())
    except PermissionError:
        kill_holding_processes(p.name)
        try:
            with open(p, "rb") as f:
                data = bytearray(f.read())
        except Exception as e:
            return False, f"عدم دسترسی به فایل: {e}"
    except Exception as e:
        return False, f"خطا در خواندن فایل: {e}"

    field_count = data.count(SIG_FIELD_UNPATCHED)
    proxy_count = data.count(SIG_PROXY_UNPATCHED)

    if field_count == 0 and data.count(SIG_FIELD_PATCHED) > 0:
        return True, "این فایل قبلاً پچ شده است."

    if field_count == 0:
        return False, "امضای ineligible در این باینری یافت نشد (احتمالاً نسخه متفاوت است)."

    # جایگزینی امضاها
    new_data = bytes(data).replace(SIG_FIELD_UNPATCHED, SIG_FIELD_PATCHED)
    if proxy_count > 0:
        new_data = new_data.replace(SIG_PROXY_UNPATCHED, SIG_PROXY_PATCHED)

    success, msg = _safe_write_atomic(p, new_data)
    if success:
        _BINARY_STATUS_CACHE.clear()
        return True, f"پچ با موفقیت انجام شد ({field_count} امضا ویرایش شد)."
    else:
        return False, f"خطا در ذخیره‌سازی فایل پچ شده: {msg}"



def unpatch_binary_file(filepath: str) -> Tuple[bool, str]:
    """
    برگرداندن فایل باینری به حالت اولیه و دست‌نخورده (Unpatch)
    """
    p = Path(filepath)
    if not p.exists():
        return False, f"فایل وجود ندارد: {filepath}"

    try:
        with open(p, "rb") as f:
            data = bytearray(f.read())
    except PermissionError:
        kill_holding_processes(p.name)
        try:
            with open(p, "rb") as f:
                data = bytearray(f.read())
        except Exception as e:
            return False, f"عدم دسترسی به فایل: {e}"
    except Exception as e:
        return False, f"خطا در خواندن فایل: {e}"

    field_count = data.count(SIG_FIELD_PATCHED)
    proxy_count = data.count(SIG_PROXY_PATCHED)

    if field_count == 0 and data.count(SIG_FIELD_UNPATCHED) > 0:
        return True, "فایل در حالت دست‌نخورده و اصلی قرار دارد."

    if field_count == 0:
        return False, "امضای پچ شده inexigible در این باینری یافت نشد."

    # بازگردانی بایت‌ها
    new_data = bytes(data).replace(SIG_FIELD_PATCHED, SIG_FIELD_UNPATCHED)
    if proxy_count > 0:
        new_data = new_data.replace(SIG_PROXY_PATCHED, SIG_PROXY_UNPATCHED)

    success, msg = _safe_write_atomic(p, new_data)
    if success:
        _BINARY_STATUS_CACHE.clear()
        return True, f"فایل با موفقیت به حالت اولیه بازگردانده شد ({field_count} مورد بازیابی شد)."
    else:
        return False, f"خطا در بازگردانی فایل: {msg}"

