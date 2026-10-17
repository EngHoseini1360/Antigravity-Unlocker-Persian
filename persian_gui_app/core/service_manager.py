"""
مدیریت سرویس‌های سیستمی ویندوز، قوانین DNS NRPT، بررسی دسترسی ادمین و وضعیت ارتباط شبکه
"""

import ctypes
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from .settings_manager import (
    get_appdata_dir,
    get_forwarder_log_path,
    get_gate_file_path,
    get_watchdog_log_path,
)


def is_admin() -> bool:
    """بررسی اینکه آیا برنامه در حال حاضر با دسترسی Administrator اجرا شده است یا خیر"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_as_admin() -> None:
    """درخواست ارتقا به دسترسی مدیر (UAC) و اجرای مجدد برنامه"""
    if is_admin():
        return

    # مسیر اسکریپت یا مفسر
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    executable = sys.executable

    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        executable,
        f'"{script}" {params}',
        None,
        1  # SW_SHOWNORMAL
    )
    sys.exit(0)


_NRPT_CACHE = None
_NRPT_CACHE_TIME = 0.0

_RELAY_CACHE = None
_RELAY_CACHE_TIME = 0.0


def check_nrpt_rules(force: bool = False) -> Tuple[bool, str]:
    """بررسی وجود قوانین تفکیک DNS (NRPT) در ویندوز برای دامنه cloudcode-pa.googleapis.com (دارای کش)"""
    global _NRPT_CACHE, _NRPT_CACHE_TIME
    now = time.time()
    if not force and _NRPT_CACHE is not None and (now - _NRPT_CACHE_TIME < 10.0):
        return _NRPT_CACHE

    cmd = 'powershell -NoProfile -Command "Get-DnsClientNrptRule -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Namespace"'
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        output = res.stdout.lower()
        if "cloudcode-pa.googleapis.com" in output:
            result = (True, "قوانین DNS NRPT برای دامنه‌های اختصاصی گوگل فعال است.")
        else:
            result = (False, "قوانین تفکیک DNS در حال حاضر در سیستم ثبت نشده‌اند.")
    except Exception as e:
        result = (False, f"خطا در بررسی NRPT: {e}")

    _NRPT_CACHE = result
    _NRPT_CACHE_TIME = now
    return result


def check_port_listening(host: str = "127.0.0.1", port: int = 53129, timeout: float = 0.1) -> bool:
    """بررسی باز بودن پورت لوکال رله یا پروکسی"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except Exception:
        return False


def is_relay_service_running(force: bool = False) -> bool:
    """بررسی اینکه آیا پروسه رله DNS یا پروکسی لوکال در حال اجراست (سریع و دارای کش)"""
    global _RELAY_CACHE, _RELAY_CACHE_TIME
    now = time.time()
    if not force and _RELAY_CACHE is not None and (now - _RELAY_CACHE_TIME < 4.0):
        return _RELAY_CACHE

    # ۱. ابتدا بررسی سریع پورت با سوکت شبکه
    if check_port_listening("127.0.0.1", 53129, timeout=0.08):
        _RELAY_CACHE = True
        _RELAY_CACHE_TIME = now
        return True

    # ۲. بررسی پروسه ag_dns.exe
    try:
        res = subprocess.run(
            'tasklist /FI "IMAGENAME eq ag_dns.exe" /NH',
            shell=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        running = "ag_dns.exe" in res.stdout.lower()
    except Exception:
        running = False

    _RELAY_CACHE = running
    _RELAY_CACHE_TIME = now
    return running



def test_google_cloudcode_connection(proxy_url: Optional[str] = None, timeout: float = 4.0) -> Tuple[bool, str, float]:
    """
    تست اتصال به سرور cloudcode-pa.googleapis.com و محاسبه پینگ (زمان پاسخ‌دهی)
    """
    target_url = "https://cloudcode-pa.googleapis.com/generate_204"
    start_time = time.time()
    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "AntigravityUnlocker/2.24.0"}
        )

        handlers = []
        if proxy_url:
            handlers.append(urllib.request.ProxyHandler({
                "http": proxy_url,
                "https": proxy_url
            }))
        
        opener = urllib.request.build_opener(*handlers)
        with opener.open(req, timeout=timeout) as resp:
            elapsed_ms = round((time.time() - start_time) * 1000, 1)
            code = resp.getcode()
            return True, f"اتصال برقرار است (کد {code})", elapsed_ms
    except urllib.error.HTTPError as e:
        elapsed_ms = round((time.time() - start_time) * 1000, 1)
        # حتی خطای 404 یا 401 نشان می‌دهد ارتباط با سرور گوگل برقرار است و هاست فیلتر نیست
        return True, f"سرور پاسخ داد (کد {e.code})", elapsed_ms
    except Exception as e:
        elapsed_ms = round((time.time() - start_time) * 1000, 1)
        return False, f"عدم پاسخگویی سرور: {e}", elapsed_ms


try:
    from .log_translator import translate_log_text
except (ImportError, ValueError):
    from core.log_translator import translate_log_text


def read_file_tail(filepath: Path, max_lines: int = 150) -> str:
    """خواندن آخرین خطوط یک فایل لاگ و ترجمه آن به زبان فارسی"""
    if not filepath.exists():
        return "فایل لاگ هنوز ایجاد نشده است."
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            raw_text = "".join(lines[-max_lines:])
            return translate_log_text(raw_text)
    except Exception as e:
        return f"خطا در خواندن لاگ: {e}"


def get_forwarder_logs(max_lines: int = 200) -> str:
    return read_file_tail(get_forwarder_log_path(), max_lines)


def get_watchdog_logs(max_lines: int = 200) -> str:
    return read_file_tail(get_watchdog_log_path(), max_lines)


def get_diagnostic_report() -> str:
    """تولید یک گزارش تشخیصی کامل به زبان فارسی جهت بررسی مشکلات یا اشتراک‌گذاری"""
    admin_stat = "بله (Administrator)" if is_admin() else "خیر (کاربر معمولی)"
    nrpt_stat, nrpt_msg = check_nrpt_rules()
    relay_stat = "در حال اجرا (پورت 53129 فعال)" if is_relay_service_running() else "غیرفعال"
    
    report_lines = [
        "========================================",
        "گزارش تشخیصی Antigravity Unlocker - نسخه فارسی",
        "برنامه‌نویس: AliasgharHoseini",
        "========================================",
        f"دسترسی ادمین (Administrator): {admin_stat}",
        f"وضعیت سرویس رله DNS / پروکسی: {relay_stat}",
        f"وضعیت قوانین تفکیک DNS (NRPT): {'فعال' if nrpt_stat else 'غیرفعال'} ({nrpt_msg})",
        f"مسیر ذخیره تنظیمات: {get_appdata_dir()}",
        "",
        "--- آخرین وضعیت دروازه شبکه (gate.json) ---",
        read_file_tail(get_gate_file_path(), 30),
        "",
        "--- آخرین رخدادهای رله (forwarder.log) ---",
        read_file_tail(get_forwarder_log_path(), 40),
        "",
        "--- آخرین رخدادهای نگهبان (watchdog.log) ---",
        read_file_tail(get_watchdog_log_path(), 30),
        "========================================",
    ]
    return "\n".join(report_lines)

