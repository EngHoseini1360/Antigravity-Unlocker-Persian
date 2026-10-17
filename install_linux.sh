#!/usr/bin/env bash
# ========================================================
# اسکریپت نصب و راه‌اندازی نسخه لینوکس Antigravity Unlocker (فارسی)
# توسعه‌دهنده: AliasgharHoseini (https://github.com/EngHoseini1360)
# ========================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "========================================================"
echo "🇮🇷 نصب و آماده‌سازی Antigravity Unlocker در لینوکس"
echo "👨‍💻 توسعه‌دهنده: AliasgharHoseini"
echo "========================================================"

# اعطای دسترسی اجرایی به اسکریپت‌ها
chmod +x run_persian_gui.sh

# نصب خودکار پیش‌نیازها بر اساس پکیج منیجر توزیع
if command -v apt-get >/dev/null 2>&1; then
    echo "📦 توزیع مبتنی بر Debian/Ubuntu شناسایی شد."
    read -p "آیا مایل به نصب پیش‌نیازها (python3-pyqt6) با apt هستید؟ (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pyqt6
    fi
elif command -v pacman >/dev/null 2>&1; then
    echo "📦 توزیع مبتنی بر Arch Linux شناسایی شد."
    read -p "آیا مایل به نصب پیش‌نیازها (python-pyqt6) با pacman هستید؟ (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        sudo pacman -S --needed python python-pyqt6
    fi
elif command -v dnf >/dev/null 2>&1; then
    echo "📦 توزیع مبتنی بر Fedora/RHEL شناسایی شد."
    read -p "آیا مایل به نصب پیش‌نیازها (python3-pyqt6) با dnf هستید؟ (y/n): " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        sudo dnf install -y python3 python3-pyqt6
    fi
fi

# ایجاد میانبر دسکتاپ (Desktop Shortcut) در لینوکس
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

DESKTOP_FILE="$DESKTOP_DIR/antigravity-unlocker-persian.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Antigravity Unlocker (نسخه فارسی)
Comment=ابزار رفع تحریم و فعال‌سازی هوش مصنوعی گوگل برای Antigravity و Antigravity IDE
Exec=bash "$DIR/run_persian_gui.sh"
Path=$DIR
Icon=$DIR/icon.ico
Terminal=false
Categories=Development;Utility;
Keywords=antigravity;google;ai;unlock;persian;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "✅ نصب با موفقیت انجام شد!"
echo "📌 میانبر برنامه به منوی برنامه‌های لینوکس اضافه شد: $DESKTOP_FILE"
echo "🚀 برای اجرای برنامه می‌توانید از دستور زیر استفاده کنید:"
echo "   ./run_persian_gui.sh"
echo ""
