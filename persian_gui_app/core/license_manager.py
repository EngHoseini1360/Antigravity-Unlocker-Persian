"""
مدیریت لایسنس و کلیدهای فعال‌سازی Antigravity Unlocker
الگوریتم بر اساس هش SHA256 و سالت نسخه پروژه پیاده‌سازی شده است.
"""

import hashlib
import random
import string
from typing import Optional

LICENSE_BASE_SECRET: str = ")Q.QFyU+oOs#Z:jmtxonGfZi+w#|XG4<"
LICENSE_VERSION_SEP: str = "::"
DEFAULT_VERSION: str = "2.24.0"


def get_key_secret(version: str = DEFAULT_VERSION) -> str:
    """تولید سکرت ترکیبی همراه با نسخه نرم‌افزار"""
    return f"{LICENSE_BASE_SECRET}{LICENSE_VERSION_SEP}{version}"


def clean_key(key: str) -> str:
    """حذف خط تیره‌ها، فاصله‌ها و تبدیل به حروف بزرگ"""
    return "".join(c for c in key if c.isalnum()).upper()


def format_key(key: str) -> str:
    """فرمت‌بندی کلید به شکل چهار حرفی: XXXX-XXXX-XXXX-XXXX-XXXX-XXXX"""
    cleaned = clean_key(key)
    if len(cleaned) == 24:
        return "-".join(cleaned[i:i + 4] for i in range(0, 24, 4))
    return key


def verify_key(key: str, version: str = DEFAULT_VERSION) -> bool:
    """
    بررسی معتبر بودن کلید فعال‌سازی برای نسخه مشخص شده.
    طول کلید باید ۲۴ کاراکتر باشد: ۱۲ کاراکتر نانس + ۱۲ کاراکتر هش.
    """
    cleaned = clean_key(key)
    if len(cleaned) != 24:
        return False

    nonce = cleaned[:12]
    secret = get_key_secret(version)
    hasher = hashlib.sha256()
    hasher.update(nonce.encode("utf-8"))
    hasher.update(secret.encode("utf-8"))
    expected = hasher.hexdigest().upper()[:12]

    # مقایسه ایمن
    result = 0
    for x, y in zip(cleaned[12:], expected):
        result |= ord(x) ^ ord(y)
    return result == 0


def generate_key(nonce: Optional[str] = None, version: str = DEFAULT_VERSION) -> str:
    """
    تولید یک کلید فعال‌سازی معتبر و کاملاً قانونی برای نسخه جاری.
    بدون نیاز به مراجعه به تلگرام، کاربر می‌تواند مستقیماً کلید معتبر تولید کند.
    """
    if not nonce or len(clean_key(nonce)) != 12:
        chars = string.ascii_uppercase + string.digits
        nonce = "".join(random.choice(chars) for _ in range(12))
    else:
        nonce = clean_key(nonce)[:12]

    secret = get_key_secret(version)
    hasher = hashlib.sha256()
    hasher.update(nonce.encode("utf-8"))
    hasher.update(secret.encode("utf-8"))
    signature = hasher.hexdigest().upper()[:12]

    return f"{nonce}{signature}"
