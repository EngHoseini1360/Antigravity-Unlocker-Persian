#!/usr/bin/env bash
# ========================================================
# اسکریپت نصب و راه‌اندازی نسخه مک‌اواس (macOS) Antigravity Unlocker (فارسی)
# توسعه‌دهنده: AliasgharHoseini (https://github.com/EngHoseini1360)
# ========================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "========================================================"
echo "🇮🇷 نصب و راه‌اندازی Antigravity Unlocker در مک‌اواس (macOS)"
echo "👨‍💻 توسعه‌دهنده: AliasgharHoseini"
echo "========================================================"

# اعطای دسترسی اجرایی به اسکریپت‌های مک
chmod +x run_persian_gui_mac.command run_persian_gui.sh

# نصب پیش‌نیازها از طریق Homebrew در صورت وجود
if command -v brew >/dev/null 2>&1; then
    echo "📦 پکیج‌منیجر Homebrew شناسایی شد."
    read -p "آیا مایل به نصب پایتون و PyQt6 از طریق Homebrew هستید؟ (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        brew install python pyqt6
    fi
else
    echo "💡 توصیه: برای مدیریت آسان پکیج‌ها در مک، Homebrew را نصب نمایید (https://brew.sh)."
    pip3 install PyQt6 || true
fi

echo ""
echo "✅ آماده‌سازی با موفقیت انجام شد!"
echo "🚀 برای اجرای برنامه در مک، کافیست روی فایل زیر دو بار کلیک کنید:"
echo "   run_persian_gui_mac.command"
echo "یا در ترمینال دستور زیر را وارد نمایید:"
echo "   ./run_persian_gui_mac.command"
echo ""
