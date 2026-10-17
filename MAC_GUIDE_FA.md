# 🍏 راهنمای جامع استفاده از Antigravity Unlocker در مک‌اواس (macOS)

این نرم‌افزار به صورت **کاملاً بومی (Native) و چندسکویی (Cross-Platform)** برای سیستم‌عامل **macOS** بهینه‌سازی شده است و بدون هیچ مشکلی روی هر دو معماری پردازنده‌های **Intel (x86_64)** و چیپ‌های **Apple Silicon (M1, M2, M3, M4 - ARM64)** اجرا می‌شود.

---

## 👨‍💻 برنامه‌نویس و توسعه‌دهنده
* **طراح و توسعه‌دهنده:** **AliasgharHoseini** ([@EngHoseini1360](https://github.com/EngHoseini1360))
* **مجوز:** MIT License

---

## 📦 پیش‌نیازها و نصب در مک (macOS)

برای اجرای برنامه در مک، تنها به **Python 3.10+** و کتابخانه گرافیکی **PyQt6** نیاز دارید:

### روش اول: با استفاده از Homebrew (سریع‌ترین روش)
اگر از ابزار محبوب [Homebrew](https://brew.sh) در مک استفاده می‌کنید، کافیست در ترمینال دستور زیر را اجرا کنید:
```bash
brew install python pyqt6
```

### روش دوم: با استفاده از Pip
```bash
pip3 install PyQt6
```

---

## 🚀 روش‌های اجرای برنامه در مک

### روش اول: دوبار کلیک در فایندر (Finder) — بسیار ساده
کافیست در پوشه برنامه، روی فایل زیر دو بار کلیک نمایید:
```text
run_persian_gui_mac.command
```
این فایل به صورت خودکار ترمینال مک را باز کرده و برنامه گرافیکی فارسی را نمایش می‌دهد.

> **نکته امنیتی مک (Gatekeeper):** اگر در اولین اجرا با پیام امنیتی مک مبنی بر اجازه اجرا مواجه شدید، در ترمینال دستور زیر را برای اعطای دسترسی وارد نمایید:
> ```bash
> chmod +x run_persian_gui_mac.command
> xattr -cr run_persian_gui_mac.command
> ```

### روش دوم: اجرای آسان از طریق اسکریپت در ترمینال
```bash
chmod +x run_persian_gui_mac.command
./run_persian_gui_mac.command
```

### روش سوم: اجرای مستقیم با مفسر پایتون
```bash
python3 persian_gui_app/main.py
```

---

## 🛡️ نحوه عملکرد فنی پچ در مک‌اواس (macOS)

1. **شناسایی خودکار بسته‌های نرم‌افزاری `.app`:**
   برنامه به صورت هوشمند مسیرهای رسمی نصب Antigravity در مک را بررسی می‌کند:
   - `/Applications/Antigravity.app`
   - `/Applications/Antigravity IDE.app`
   - `~/Applications/Antigravity.app`
   - دایرکتوری `~/Library/Application Support/Antigravity`
   - افزونه‌های VS Code و Cursor در `~/.vscode/extensions`

2. **پچ اتمیک باینری‌های Mach-O (Mach-O Binaries):**
   - فایل‌های اجرایی Language Server موجود در مسیر `Contents/Resources/bin/` یا `Contents/MacOS/` شناسایی می‌شوند (هم نسخه x64 و هم نسخه بومی arm64 برای چیپ‌های M1/M2/M3).
   - کلمه `ineligible` بدون تغییر در طول بایت‌ها و ساختار فایل Mach-O به `inexigible` تبدیل می‌شود.
   - متغیر محیطی `https_proxy` به `AG_LS_PROXY` تبدیل می‌گردد تا ترافیک سایر برنامه‌ها (مانند Safari، Chrome، Slack، Git) کاملاً ایزوله بماند.

3. **تفکیک مسیر ترافیک در مک:**
   - ترافیک هوش مصنوعی گوگل از طریق مسیر اختصاصی و پروکسی انتخابی شما (مثل V2Ray یا Clash) عبور کرده و اینترنت سراسری مک بدون تغییر کار خواهد کرد.

---

## ❓ رفع اشکال و سوالات متداول در مک

### خطای Operation not permitted یا Permission Denied:
اگر نرم‌افزار Antigravity در پوشه اصلی `/Applications` نصب شده باشد، ممکن است سیستم‌عامل برای پچ فایل به دسترسی مدیر نیاز داشته باشد. کافیست:
```bash
sudo python3 persian_gui_app/main.py
```
یا از داخل برنامه، روی دکمه نارنجی‌رنگ بالای صفحه **«احراز هویت با دسترسی Admin (مک)»** کلیک کنید و رمز عبور مک یا Touch ID را تأیید نمایید.

---

## 📄 لایسنس
توسعه یافته بر پایه مجوز رسمی **MIT License** توسط **AliasgharHoseini**.
