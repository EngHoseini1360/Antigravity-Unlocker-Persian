#!/usr/bin/env bash
# ========================================================
# اسکریپت اجرای نسخه مک‌اواس (macOS) Antigravity Unlocker (فارسی)
# توسعه‌دهنده: AliasgharHoseini (https://github.com/EngHoseini1360)
# ========================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "========================================================"
echo "🇮🇷 اجرای Antigravity Unlocker — نسخه فارسی (macOS)"
echo "👨‍💻 توسعه‌دهنده: AliasgharHoseini"
echo "========================================================"

# یافتن مفسر پایتون ۳ در مک (مسیرهای Homebrew یا سیستم)
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif [ -f "/opt/homebrew/bin/python3" ]; then
    PYTHON_CMD="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PYTHON_CMD="/usr/local/bin/python3"
else
    echo "❌ خطا: پایتون ۳ در مک یافت نشد!"
    echo "می‌توانید با دستور زیر پایتون را نصب کنید:"
    echo "   brew install python pyqt6"
    exit 1
fi

# بررسی وجود PyQt6
if ! $PYTHON_CMD -c "import PyQt6" >/dev/null 2>&1; then
    echo "⚠️ کتابخانه PyQt6 نصب نیست. در حال نصب خودکار..."
    $PYTHON_CMD -m pip install PyQt6 || {
        echo "❌ برای نصب در مک می‌توانید از Homebrew استفاده کنید:"
        echo "   brew install pyqt6"
        exit 1
    }
fi

# اجرای برنامه
exec $PYTHON_CMD persian_gui_app/main.py "$@"
