"""
تب داشبورد اصلی: وضعیت زنده، فعال‌سازی یک‌کلیکه و سوئیچ‌های محوری
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from ..core.detector import scan_all_installs
    from ..core.license_manager import verify_key
    from ..core.patcher import (
        check_binary_status,
        patch_binary_file,
        unpatch_binary_file,
    )
    from ..core.service_manager import is_admin, is_relay_service_running, run_as_admin
    from ..core.settings_manager import load_settings, save_settings
    from .components import CardWidget, StatusBadge, SwitchRow
except (ImportError, ValueError):
    from core.detector import scan_all_installs
    from core.license_manager import verify_key
    from core.patcher import (
        check_binary_status,
        patch_binary_file,
        unpatch_binary_file,
    )
    from core.service_manager import is_admin, is_relay_service_running, run_as_admin
    from core.settings_manager import load_settings, save_settings
    from ui.components import CardWidget, StatusBadge, SwitchRow



class DashboardTab(QWidget):
    status_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 16)
        self.layout.setSpacing(14)

        self._build_status_banner()
        self._build_action_buttons()
        self._build_switches_card()
        self._build_summary_card()

        self.refresh_status()

    def _build_status_banner(self):
        """بنر بالایی نشان‌دهنده وضعیت کلی سیستم"""
        self.banner_frame = QFrame()
        self.banner_frame.setObjectName("StatusBannerCard")
        b_layout = QHBoxLayout(self.banner_frame)
        b_layout.setContentsMargins(20, 16, 20, 16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        self.banner_title = QLabel("در حال بررسی وضعیت سیستم...")
        self.banner_title.setObjectName("HeaderTitle")
        text_layout.addWidget(self.banner_title)

        self.banner_desc = QLabel("لطفاً چند لحظه صبر کنید...")
        self.banner_desc.setObjectName("SubTitle")
        text_layout.addWidget(self.banner_desc)

        b_layout.addLayout(text_layout)
        b_layout.addStretch()

        # نشانگرهای دسترسی ادمین و لایسنس
        badges_layout = QVBoxLayout()
        badges_layout.setSpacing(6)
        badges_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.badge_status = StatusBadge("در حال ارزیابی", "warning")
        self.badge_admin = StatusBadge("دسترسی عادی", "neutral")

        badges_layout.addWidget(self.badge_status)
        badges_layout.addWidget(self.badge_admin)
        b_layout.addLayout(badges_layout)

        self.layout.addWidget(self.banner_frame)

    def _build_action_buttons(self):
        """کارت دکمه‌های اقدام سریع و یک‌کلیکه"""
        card = CardWidget("عملیات سریع و یکپارچه", "اعمال تغییرات روی تمامی نسخه‌های نصب‌شده با یک کلیک", "⚡")
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.btn_enable_all = QPushButton("  ⚡ فعال‌سازی هوشمند همه موارد (پچ و رفع تحریم)  ")
        self.btn_enable_all.setObjectName("PrimaryButton")
        self.btn_enable_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_enable_all.clicked.connect(self.on_enable_all_clicked)
        btn_layout.addWidget(self.btn_enable_all)

        self.btn_disable_all = QPushButton("  🔄 بازگردانی فایل‌ها به حالت اولیه (Unpatch)  ")
        self.btn_disable_all.setObjectName("DangerButton")
        self.btn_disable_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_disable_all.clicked.connect(self.on_disable_all_clicked)
        btn_layout.addWidget(self.btn_disable_all)

        self.btn_refresh = QPushButton("  🔍 بررسی مجدد وضعیت  ")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_status)
        btn_layout.addWidget(self.btn_refresh)

        card.add_layout(btn_layout)
        self.layout.addWidget(card)

    def _build_switches_card(self):
        """کارت سوئیچ‌های اصلی تنظیمات"""
        card = CardWidget("کلیدهای اصلی عملکرد نرم‌افزار", "کنترل رفتار پچ کلاینت، نگهبان و پروکسی محلی", "⚙️")

        self.switch_client_patch = SwitchRow(
            "رفع تحریم و باز کردن قفل حساب کاربری گوگل (Client Patch)",
            "حذف خطای ۴۰۰ (User location is not supported) از طریق ویرایش امضای protobuf در باینری language_server",
            True
        )
        self.switch_client_patch.toggled.connect(self._on_switch_client_patch)
        card.add_widget(self.switch_client_patch)

        self.switch_auto_patch = SwitchRow(
            "پچ خودکار پس از آپدیت نرم‌افزار (Watchdog Auto-Patch)",
            "نگهبانی دائمی و اعمال خودکار پچ در صورت بروزرسانی Antigravity توسط گوگل",
            True
        )
        self.switch_auto_patch.toggled.connect(self._on_switch_auto_patch)
        card.add_widget(self.switch_auto_patch)

        self.switch_local_proxy = SwitchRow(
            "پروکسی محلی و هدایت ترافیک (Local Proxy / AG_LS_PROXY)",
            "هدایت درخواست‌های افزونه به سرویس اختصاصی سیستم بدون تغییر پراکسی سراسری ویندوز",
            False
        )
        self.switch_local_proxy.toggled.connect(self._on_switch_local_proxy)
        card.add_widget(self.switch_local_proxy)

        self.layout.addWidget(card)

    def _build_summary_card(self):
        """خلاصه وضعیت مؤلفه‌ها"""
        card = CardWidget("خلاصه وضعیت سیستم و سرویس‌ها", "جزئیات اجزای اجرایی و ارتباطی", "📊")
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)

        # ستون ۱: باینری‌ها
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("<b>وضعیت باینری‌ها:</b>"))
        self.lbl_binaries_stat = QLabel("در حال اسکن...")
        self.lbl_binaries_stat.setStyleSheet("color: #94a3b8;")
        col1.addWidget(self.lbl_binaries_stat)
        summary_layout.addLayout(col1)

        # ستون ۲: لایسنس
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("<b>کلید فعال‌سازی:</b>"))
        self.lbl_license_stat = QLabel("در حال بررسی...")
        self.lbl_license_stat.setStyleSheet("color: #94a3b8;")
        col2.addWidget(self.lbl_license_stat)
        summary_layout.addLayout(col2)

        # ستون ۳: سرویس پس‌زمینه
        col3 = QVBoxLayout()
        col3.addWidget(QLabel("<b>سرویس رله محلی:</b>"))
        self.lbl_relay_stat = QLabel("در حال بررسی...")
        self.lbl_relay_stat.setStyleSheet("color: #94a3b8;")
        col3.addWidget(self.lbl_relay_stat)
        summary_layout.addLayout(col3)

        card.add_layout(summary_layout)
        self.layout.addWidget(card)

    def refresh_status(self):
        """بازخوانی کامل وضعیت جاری سیستم"""
        settings = load_settings()

        # تنظیم وضعیت سوئیچ‌ها بر اساس فایل
        self.switch_client_patch.setChecked(settings.get("client_patch", True))
        self.switch_auto_patch.setChecked(settings.get("auto_patch", True))
        self.switch_local_proxy.setChecked(settings.get("local_proxy", False))

        # بررسی دسترسی ادمین
        admin = is_admin()
        if admin:
            self.badge_admin.set_status("دسترسی Administrator ✓", "success")
        else:
            self.badge_admin.set_status("کاربر معمولی (فاقد ادمین)", "warning")

        # اسکن باینری‌ها
        installs = scan_all_installs()
        total_binaries = 0
        patched_binaries = 0

        for inst in installs:
            for b_path in inst["binaries"]:
                total_binaries += 1
                stat = check_binary_status(b_path)
                if stat["status"] == "patched":
                    patched_binaries += 1

        # وضعیت لایسنس
        key = settings.get("license_key", "")
        valid_license = verify_key(key)
        if valid_license:
            self.lbl_license_stat.setText("کلید معتبر است ✓")
            self.lbl_license_stat.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_license_stat.setText("کلید نامعتبر یا ثبت‌نشده")
            self.lbl_license_stat.setStyleSheet("color: #ef4444; font-weight: bold;")

        # وضعیت رله
        relay_on = is_relay_service_running()
        if relay_on:
            self.lbl_relay_stat.setText("فعال و در حال شنود (پورت 53129) ✓")
            self.lbl_relay_stat.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_relay_stat.setText("سرویس رله متوقف است")
            self.lbl_relay_stat.setStyleSheet("color: #94a3b8;")

        # خلاصه باینری‌ها
        if total_binaries == 0:
            self.lbl_binaries_stat.setText("هیچ نسخه نصب‌شده‌ای یافت نشد!")
            self.lbl_binaries_stat.setStyleSheet("color: #ef4444;")
        else:
            self.lbl_binaries_stat.setText(f"{patched_binaries} از {total_binaries} فایل پچ شده‌اند")
            if patched_binaries == total_binaries:
                self.lbl_binaries_stat.setStyleSheet("color: #10b981; font-weight: bold;")
            elif patched_binaries > 0:
                self.lbl_binaries_stat.setStyleSheet("color: #f59e0b; font-weight: bold;")
            else:
                self.lbl_binaries_stat.setStyleSheet("color: #ef4444; font-weight: bold;")

        # بروزرسانی بنر بالایی
        if total_binaries > 0 and patched_binaries == total_binaries:
            self.banner_title.setText("Antigravity آماده به کار و رفع تحریم شده است")
            self.banner_desc.setText("تمامی نسخه‌های نصب‌شده با موفقیت پچ شده‌اند و محدودیت منطقه برداشته شده است.")
            self.banner_title.setStyleSheet("color: #10b981;")
            self.badge_status.set_status("کاملاً آماده و فعال ✓", "success")
        elif patched_binaries > 0:
            self.banner_title.setText("برخی فایل‌ها پچ شده و برخی پچ نشده‌اند")
            self.banner_desc.setText("برای رفع کامل تحریم روی دکمه «فعال‌سازی هوشمند همه موارد» کلیک کنید.")
            self.banner_title.setStyleSheet("color: #f59e0b;")
            self.badge_status.set_status("پچ جزئی", "warning")
        else:
            self.banner_title.setText("محدودیت ریجن فعال است (نیاز به پچ)")
            self.banner_desc.setText("برای شروع، دکمه «فعال‌سازی هوشمند همه موارد» را بزنید تا برنامه پچ شود.")
            self.banner_title.setStyleSheet("color: #ef4444;")
            self.badge_status.set_status("غیرفعال و مسدود", "danger")

    def update_license_only(self, settings: dict = None):
        """بروزرسانی وضعیت کلید لایسنس به صورت آنی و سبک"""
        if settings is None:
            settings = load_settings()
        key = settings.get("license_key", "")
        valid_license = verify_key(key)
        if valid_license:
            self.lbl_license_stat.setText("کلید معتبر است ✓")
            self.lbl_license_stat.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_license_stat.setText("کلید نامعتبر یا ثبت‌نشده")
            self.lbl_license_stat.setStyleSheet("color: #ef4444; font-weight: bold;")


    def on_enable_all_clicked(self):

        """اجرای عملیات پچ همگانی و فعال‌سازی تنظیمات"""
        installs = scan_all_installs()
        if not installs:
            QMessageBox.warning(self, "خطا", "هیچ نسخه نصب شده‌ای از Antigravity در سیستم یافت نشد.")
            return

        success_count = 0
        error_msgs = []

        for inst in installs:
            for b_path in inst["binaries"]:
                ok, msg = patch_binary_file(b_path)
                if ok:
                    success_count += 1
                else:
                    error_msgs.append(f"{inst['label']}: {msg}")

        # فعال‌سازی تنظیمات
        settings = load_settings()
        settings["client_patch"] = True
        settings["auto_patch"] = True
        save_settings(settings)

        self.refresh_status()
        self.status_changed.emit()

        if error_msgs:
            QMessageBox.warning(
                self,
                "گزارش پچ",
                f"پچ باینری‌ها پایان یافت:\n{success_count} فایل با موفقیت پچ شد.\n\nخطاها:\n" + "\n".join(error_msgs)
            )
        else:
            QMessageBox.information(
                self,
                "موفقیت",
                f"عملیات با موفقیت انجام شد!\n{success_count} فایل اجرایی با موفقیت پچ شدند.\nاکنون می‌توانید Antigravity را باز کرده و با اکانت گوگل خود بدون VPN وارد شوید."
            )

    def on_disable_all_clicked(self):
        """برگرداندن همه فایل‌ها به حالت دست‌نخورده"""
        reply = QMessageBox.question(
            self,
            "تأیید بازگردانی",
            "آیا مطمئن هستید که می‌خواهید تمام فایل‌ها را به حالت اصلی (قبل از پچ) بازگردانید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        installs = scan_all_installs()
        success_count = 0
        error_msgs = []

        for inst in installs:
            for b_path in inst["binaries"]:
                ok, msg = unpatch_binary_file(b_path)
                if ok:
                    success_count += 1
                else:
                    error_msgs.append(f"{inst['label']}: {msg}")

        settings = load_settings()
        settings["client_patch"] = False
        save_settings(settings)

        self.refresh_status()
        self.status_changed.emit()

        if error_msgs:
            QMessageBox.warning(
                self,
                "گزارش بازگردانی",
                f"بازگردانی پایان یافت:\n{success_count} فایل بازیابی شد.\n\nخطاها:\n" + "\n".join(error_msgs)
            )
        else:
            QMessageBox.information(
                self,
                "موفقیت",
                f"تمام فایل‌های اجرایی ({success_count} فایل) به حالت اولیه بازگردانده شدند."
            )

    def _on_switch_client_patch(self, state: bool):
        settings = load_settings()
        settings["client_patch"] = state
        save_settings(settings)

    def _on_switch_auto_patch(self, state: bool):
        settings = load_settings()
        settings["auto_patch"] = state
        save_settings(settings)

    def _on_switch_local_proxy(self, state: bool):
        settings = load_settings()
        settings["local_proxy"] = state
        save_settings(settings)
