"""
تب راهنما، آموزش گام‌به‌گام و پرسش‌های متداول به زبان فارسی
"""

from PyQt6.QtWidgets import QTextBrowser, QVBoxLayout, QWidget

GUIDE_HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="utf-8">
<style>
    body {
        font-family: 'Segoe UI', 'Tahoma', 'Vazirmatn', sans-serif;
        color: #e2e8f0;
        line-height: 1.8;
        font-size: 14px;
        background-color: transparent;
        padding: 10px;
    }
    h2 {
        color: #38bdf8;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 8px;
        margin-top: 24px;
    }
    h3 {
        color: #60a5fa;
        margin-top: 18px;
    }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-success { background-color: #064e3b; color: #10b981; }
    .badge-info { background-color: #172554; color: #60a5fa; }
    .box {
        background-color: #131b26;
        border: 1px solid #222f3e;
        border-radius: 10px;
        padding: 16px;
        margin: 14px 0;
    }
    ul, ol {
        padding-right: 22px;
    }
    li {
        margin-bottom: 8px;
    }
    code {
        font-family: Consolas, monospace;
        background-color: #1e293b;
        padding: 2px 6px;
        border-radius: 4px;
        color: #38bdf8;
    }
</style>
</head>
<body>

<h2>🚀 راهنمای جامع استفاده از Antigravity Unlocker</h2>

<div class="box">
    <b>هدف این ابزار چیست؟</b><br>
    این نرم‌افزار به کاربران و توسعه‌دهندگان ایرانی امکان می‌دهد بدون نیاز به تعویض ریجن اکانت گوگل و حتی بدون دردسرهای معمول قطعی VPN، به طور کامل از محیط هوش مصنوعی <b>Antigravity 2.0</b>، محیط توسعه <b>Antigravity IDE</b> و رابط خط فرمان <b>agy CLI</b> استفاده کنند.
</div>

<h3>📋 مراحل راه‌اندازی سریع در ۳ گام</h3>
<ol>
    <li><b>گام اول:</b> نرم‌افزار Antigravity را از سایت رسمی گوگل نصب کنید.</li>
    <li><b>گام دوم:</b> در تب «داشبورد» این نرم‌افزار، روی دکمه بزرگ آبی‌رنگ <b>«فعال‌سازی هوشمند همه موارد»</b> کلیک کنید. برنامه به طور خودکار فایل‌های مورد نیاز را پچ می‌کند.</li>
    <li><b>گام سوم:</b> نرم‌افزار Antigravity را باز کرده و با اکانت گوگل خود وارد شوید. مدل هوش مصنوعی بدون ارور به درخواست‌ها پاسخ خواهد داد!</li>
</ol>

<h2>🛡️ این نرم‌افزار در سیستم شما چه کاری انجام می‌دهد؟</h2>
<div class="box">
    <ul>
        <li><b>پچ Language Server:</b> عبارت <code>ineligible</code> را به <code>inexigible</code> تبدیل می‌کند. این کار محدودیت منطقه جغرافیایی را از سمت کلاینت دور می‌زند و اندازه فایل اجرایی هیچ تغییری نمی‌کند.</li>
        <li><b>پراکسی اختصاصی متغیر محیطی:</b> با تغییر <code>https_proxy</code> به <code>AG_LS_PROXY</code>، فقط افزونه Antigravity به پراکسی هدایت می‌شود و سایر نرم‌افزارهای ویندوز، مرورگرها و دستورات Git با سرعت عادی خود کار خواهند کرد.</li>
        <li><b>تفکیک ترافیک با قوانین NRPT:</b> فقط دامنه‌های <code>cloudcode-pa.googleapis.com</code> مسیردهی ویژه می‌شوند و اینترنت کلی ویندوز دستکاری نخواهد شد.</li>
    </ul>
</div>

<h2>❓ پرسش‌های متداول (FAQ)</h2>

<h3>آیا بعد از آپدیت Antigravity پچ حذف می‌شود؟</h3>
<p>
    خیر، با فعال بودن گزینه <b>«پچ خودکار پس از آپدیت» (Watchdog)</b>، به محض اینکه نسخه جدیدی از کلاینت نصب شود، نگهبان سیستم آن را شناسایی کرده و مجدداً پچ می‌کند. همچنین می‌توانید در هر زمان این رابط کاربری را باز کرده و دکمه فعال‌سازی را بزنید.
</p>

<h3>آیا کلید لایسنس پولی است؟</h3>
<p>
    خیر! لایسنس کاملاً رایگان است. کافیست در تب <b>«کلید فعال‌سازی»</b> روی دکمه <b>«تولید خودکار کلید»</b> کلیک کنید تا آنی یک کلید معتبر ۲۴ کاراکتری برای شما ساخته و ثبت شود.
</p>

<h3>🐧 نحوه اجرا و سازگاری در سیستم‌عامل‌های لینوکس (Linux)</h3>
<p>
    این نرم‌افزار به صورت کامل و بومی (Cross-Platform) از تمام توزیع‌های لینوکس (مانند Ubuntu، Debian، Arch Linux، Fedora و Manjaro) پشتیبانی می‌کند.<br>
    برای اجرا در لینوکس، کافیست اسکریپت <code>./run_persian_gui.sh</code> یا دستور <code>python3 persian_gui_app/main.py</code> را در ترمینال اجرا کنید. همچنین با اجرای <code>./install_linux.sh</code> می‌توانید پیش‌نیازها را خودکار نصب کرده و میانبر دسکتاپ برنامه را دریافت نمایید.
</p>

<h3>چگونه تغییرات را به حالت اول برگردانم؟</h3>
<p>
    در تب داشبورد دکمه قرمز رنگ <b>«بازگردانی فایل‌ها به حالت اولیه (Unpatch)»</b> وجود دارد که در کمتر از یک ثانیه تمام بایت‌ها و تنظیمات را به وضعیت اولیه شرکت گوگل بازمی‌گرداند.
</p>

<div class="box" style="border-color: #38bdf8; text-align: center;">
    <h3 style="color: #38bdf8; margin: 0 0 6px 0;">👨‍💻 توسعه‌دهنده و برنامه‌نویس رابط فارسی</h3>
    <p style="font-size: 15px; font-weight: bold; color: #ffffff; margin: 0;">AliasgharHoseini</p>
    <p style="color: #94a3b8; font-size: 12px; margin: 4px 0 0 0;">طراحی اختصاصی برای جامعه توسعه‌دهندگان ایرانی و فارسی‌زبان</p>
</div>

</body>
</html>
"""



class GuideTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 16)

        self.browser = QTextBrowser()
        self.browser.setOpenExternalLinks(True)
        self.browser.setHtml(GUIDE_HTML)
        self.browser.setStyleSheet("""
            QTextBrowser {
                background-color: #0d131d;
                border: 1px solid #202b3c;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.browser)
