"""
نقطه ورود اصلی نرم‌افزار Antigravity Unlocker - رابط کاربری گرافیکی فارسی تحت ویندوز
"""

import os
import sys

# تنظیم رمزگذاری استاندارد خروجی به UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# افزودن پوشه والد به sys.path در صورت نیاز
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from app import MainWindow


def main():
    # فعال‌سازی مقیاس‌بندی High-DPI در نمایشگرهای با رزولوشن بالا
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("Antigravity Unlocker - Persian GUI")
    app.setOrganizationName("Nova Antigravity")

    # تنظیم چینش بومی راست‌به‌چپ (RTL) برای تمامی ویجت‌ها و دیالوگ‌ها
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    # تنظیم فونت پیش‌فرض مناسب برای زبان فارسی
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()