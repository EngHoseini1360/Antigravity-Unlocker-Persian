#!/usr/bin/env bash
# ========================================================
# اسکریپت اجرای نسخه لینوکس Antigravity Unlocker (فارسی)
# توسعه‌دهنده: AliasgharHoseini (https://github.com/EngHoseini1360)
# ========================================================

set -e

# تعیین مسیر دایرکتوری جاری اسکریپت
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "========================================================"
echo "🇮🇷 اجرای Antigravity Unlocker — نسخه فارسی (لینوکس)"
echo "👨‍💻 توسعه‌دهنده: AliasgharHoseini"
echo "========================================================"

# بررسی مفسر پایتون ۳
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "❌ خطا: پایتون در سیستم شما یافت نشد!"
    echo "لطفاً پایتون ۳ را نصب کنید (مثلاً: sudo apt install python3 python3-pyqt6)"
    exit 1
fi

# بررسی وجود کتابخانه PyQt6
if ! $PYTHON_CMD -c "import PyQt6" >/dev/null 2>&1; then
    echo "⚠️ کتابخانه PyQt6 نصب نیست. در حال تلاش برای نصب..."
    $PYTHON_CMD -m pip install -r requirements.txt || {
        echo "❌ در صورت خطای مدیریت پکیج، دستور متناسب با توزیع خود را اجرا کنید:"
        echo "   در اوبونتو / دبیان: sudo apt install python3-pyqt6"
        echo "   در آرچ‌لینوکس:     sudo pacman -S python-pyqt6"
        echo "   در فدورا:          sudo dnf install python3-pyqt6"
        exit 1
    }
fi

# اجرای برنامه گرافیکی فارسی
exec $PYTHON_CMD persian_gui_app/main.py "$@"
