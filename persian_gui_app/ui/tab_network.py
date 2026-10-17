"""
تب تنظیمات شبکه، پیکربندی پروکسی اختصاصی، و بررسی وضعیت اتصال به سرورهای گوگل
"""

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from ..core.service_manager import (
        check_nrpt_rules,
        test_google_cloudcode_connection,
    )
    from ..core.settings_manager import load_settings, save_settings
    from .components import CardWidget, StatusBadge, SwitchRow
except (ImportError, ValueError):
    from core.service_manager import (
        check_nrpt_rules,
        test_google_cloudcode_connection,
    )
    from core.settings_manager import load_settings, save_settings
    from ui.components import CardWidget, StatusBadge, SwitchRow



class PingWorker(QThread):
    finished_signal = pyqtSignal(bool, str, float)

    def __init__(self, proxy_url: str = None):
        super().__init__()
        self.proxy_url = proxy_url

    def run(self):
        ok, msg, ping_ms = test_google_cloudcode_connection(self.proxy_url)
        self.finished_signal.emit(ok, msg, ping_ms)


class NetworkTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.layout = layout
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(14)

        self._build_proxy_card()
        self._build_dns_card()
        self._build_nrpt_card()

        layout.addStretch()
        self.load_network_settings()

    def _build_proxy_card(self):
        """کارت تنظیمات پراکسی اختصاصی (مانند V2Ray / Clash)"""
        card = CardWidget("پروکسی سفارشی کاربر (Custom HTTP Proxy)", "در صورت تمایل به عبور ترافیک از کانفیگ V2Ray/Xray یا ابزار تحریم‌شکن شخصی", "🌐")

        self.switch_own_proxy = SwitchRow(
            "فعال‌سازی پروکسی اختصاصی",
            "استفاده از آدرس پروکسی مشخص شده در زیر برای ارسال ترافیک Antigravity",
            True
        )
        card.add_widget(self.switch_own_proxy)

        # ردیف آدرس پروکسی
        proxy_box = QHBoxLayout()
        proxy_box.setSpacing(10)

        lbl = QLabel("آدرس پروکسی (Host:Port):")
        lbl.setStyleSheet("font-weight: 600;")
        proxy_box.addWidget(lbl)

        self.txt_proxy = QLineEdit()
        self.txt_proxy.setPlaceholderText("مثال: 127.0.0.1:10808 یا 127.0.0.1:7890")
        self.txt_proxy.setStyleSheet("font-family: Consolas, monospace; font-size: 13px;")
        proxy_box.addWidget(self.txt_proxy)

        self.btn_test_proxy = QPushButton("⚡ تست اتصال و پینگ")
        self.btn_test_proxy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_test_proxy.clicked.connect(self._test_connection)
        proxy_box.addWidget(self.btn_test_proxy)

        card.add_layout(proxy_box)

        # نتیجه تست پینگ
        self.lbl_ping_result = QLabel("")
        self.lbl_ping_result.setStyleSheet("font-size: 12px; color: #94a3b8;")
        card.add_widget(self.lbl_ping_result)

        self.layout.addWidget(card)

    def _build_dns_card(self):
        """کارت تنظیمات DNS و روتیشن"""
        card = CardWidget("سیاست‌های DNS و امنیت TLS", "تنظیم نحوه تبدیل نام دامنه و اعتبارسنجی سرورهای گوگل", "🛡️")

        self.switch_rotate = SwitchRow(
            "روتیشن و چرخش سرورهای DNS (DNS Rotation)",
            "استفاده همزمان و رقابتی از سرورهای DNS متعدد جهت تضمین سریع‌ترین پاسخ",
            True
        )
        card.add_widget(self.switch_rotate)

        self.switch_tls = SwitchRow(
            "بررسی و تطبیق گواهی امنیتی TLS (Verify TLS)",
            "اطمینان از اصالت گواهینامه‌های رسمی گوگل هنگام هدایت درخواست‌ها",
            True
        )
        card.add_widget(self.switch_tls)

        self.switch_builtin = SwitchRow(
            "مسیرهای خروجی تعبیه‌شده (Built-in Permitted Exits)",
            "استفاده از رله‌های اختصاصی داخلی جهت گذر از محدودیت‌های منطقه‌ای",
            True
        )
        card.add_widget(self.switch_builtin)

        self.layout.addWidget(card)

    def _build_nrpt_card(self):
        """کارت قوانین تفکیک نام ویندوز (NRPT)"""
        card = CardWidget("قوانین ویندوز (Windows DNS NRPT)", "تفکیک اختصاصی دامنه‌های cloudcode-pa.googleapis.com بدون دستکاری کل اینترنت سیستم", "🪟")

        row = QHBoxLayout()
        self.nrpt_badge = StatusBadge("در حال بررسی", "neutral")
        row.addWidget(self.nrpt_badge)

        self.btn_check_nrpt = QPushButton("بررسی قوانین سیستم")
        self.btn_check_nrpt.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check_nrpt.clicked.connect(self._check_nrpt)
        row.addWidget(self.btn_check_nrpt)
        row.addStretch()

        card.add_layout(row)

        self.lbl_nrpt_desc = QLabel("قوانین NRPT باعث می‌شود فقط ترافیک مربوط به هوش مصنوعی گوگل از مسیر ویژه عبور کند و مرورگرها و بازی‌های شما کاملاً عادی کار کنند.")
        self.lbl_nrpt_desc.setStyleSheet("color: #64748b; font-size: 11px;")
        self.lbl_nrpt_desc.setWordWrap(True)
        card.add_widget(self.lbl_nrpt_desc)

        # دکمه ذخیره تنظیمات
        btn_save = QPushButton("  💾 ذخیره تغییرات تنظیمات شبکه  ")
        btn_save.setObjectName("PrimaryButton")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.save_network_settings)
        card.add_widget(btn_save)

        self.layout.addWidget(card)

    def load_network_settings(self):
        """بارگذاری تنظیمات شبکه از فایل"""
        settings = load_settings()
        self.switch_own_proxy.setChecked(settings.get("own_proxy_enabled", True))
        self.txt_proxy.setText(settings.get("own_proxy", "127.0.0.1:10808"))
        self.switch_rotate.setChecked(settings.get("rotate_providers", True))
        self.switch_tls.setChecked(settings.get("verify_tls", True))
        self.switch_builtin.setChecked(settings.get("builtin_exits", True))
        self._check_nrpt()

    def save_network_settings(self):
        """ذخیره تنظیمات در فایل settings.json"""
        settings = load_settings()
        settings["own_proxy_enabled"] = self.switch_own_proxy.isChecked()
        settings["own_proxy"] = self.txt_proxy.text().strip()
        settings["rotate_providers"] = self.switch_rotate.isChecked()
        settings["verify_tls"] = self.switch_tls.isChecked()
        settings["builtin_exits"] = self.switch_builtin.isChecked()
        if save_settings(settings):
            QMessageBox.information(self, "موفقیت", "تنظیمات شبکه با موفقیت ذخیره شد.")
        else:
            QMessageBox.warning(self, "خطا", "خطا در ذخیره تنظیمات شبکه!")

    def _check_nrpt(self):
        active, msg = check_nrpt_rules()
        if active:
            self.nrpt_badge.set_status("قوانین فعال است ✓", "success")
        else:
            self.nrpt_badge.set_status("قوانین غیرفعال است", "warning")

    def _test_connection(self):
        """آزمون زنده اتصال به سرور Google Cloud Code"""
        self.btn_test_proxy.setEnabled(False)
        self.lbl_ping_result.setText("در حال برقراری ارتباط با سرور گوگل...")
        self.lbl_ping_result.setStyleSheet("color: #3b82f6;")

        proxy_str = self.txt_proxy.text().strip() if self.switch_own_proxy.isChecked() else None
        if proxy_str and not proxy_str.startswith("http"):
            proxy_str = f"http://{proxy_str}"

        self.worker = PingWorker(proxy_str)
        self.worker.finished_signal.connect(self._on_ping_finished)
        self.worker.start()

    def _on_ping_finished(self, ok: bool, msg: str, ping_ms: float):
        self.btn_test_proxy.setEnabled(True)
        if ok:
            self.lbl_ping_result.setText(f"✓ {msg} — زمان پاسخ‌دهی (Ping): {ping_ms} میلی‌ثانیه")
            self.lbl_ping_result.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_ping_result.setText(f"✗ {msg} ({ping_ms} ms)")
            self.lbl_ping_result.setStyleSheet("color: #ef4444; font-weight: bold;")
