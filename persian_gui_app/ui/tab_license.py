"""
تب مدیریت لایسنس و کلیدساز خودکار: اعتبارسنجی آنی و تولید کلید معتبر برای نسخه 2.24.0
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from ..core.license_manager import (
        DEFAULT_VERSION,
        clean_key,
        format_key,
        generate_key,
        verify_key,
    )
    from ..core.settings_manager import load_settings, save_settings
    from .components import CardWidget, StatusBadge
except (ImportError, ValueError):
    from core.license_manager import (
        DEFAULT_VERSION,
        clean_key,
        format_key,
        generate_key,
        verify_key,
    )
    from core.settings_manager import load_settings, save_settings
    from ui.components import CardWidget, StatusBadge



class LicenseTab(QWidget):
    license_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(14)

        # کارت وضعیت و مشخصات نسخه
        info_card = CardWidget("اطلاعات نسخه و سالت فعال‌سازی", "الگوریتم رمزنگاری کلید وابسته به نسخه محصول است", "ℹ️")
        v_layout = QHBoxLayout()
        v_layout.addWidget(QLabel("<b>نسخه فعلی نرم‌افزار:</b>"))
        v_lbl = QLabel(f"Antigravity Unlocker v{DEFAULT_VERSION}")
        v_lbl.setStyleSheet("color: #38bdf8; font-weight: bold;")
        v_layout.addWidget(v_lbl)
        v_layout.addStretch()

        self.badge_license = StatusBadge("بررسی نشده", "neutral")
        v_layout.addWidget(self.badge_license)
        info_card.add_layout(v_layout)
        layout.addWidget(info_card)

        # کارت وارد کردن و مدیریت کلید
        key_card = CardWidget("کلید فعال‌سازی Antigravity Unlocker", "کلید ۲۴ کاراکتری برای باز شدن کامل امکانات نرم‌افزار", "🔑")

        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("B3K87D0GWZAZB80F78E1F997")
        self.txt_key.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.txt_key.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.txt_key.setStyleSheet("""
            QLineEdit {
                direction: ltr;
                font-family: Consolas, monospace;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 2px;
            }
        """)
        self.txt_key.textChanged.connect(self._on_key_typed)
        key_card.add_widget(self.txt_key)

        self.lbl_formatted = QLabel("")
        self.lbl_formatted.setStyleSheet("font-family: Consolas, monospace; color: #94a3b8; font-size: 12px;")
        key_card.add_widget(self.lbl_formatted)


        # دکمه‌های عملیاتی کلید
        btn_box = QHBoxLayout()
        btn_box.setSpacing(10)

        self.btn_generate = QPushButton("  ⚡ تولید خودکار کلید معتبر رایگان (کلیدساز آنی)  ")
        self.btn_generate.setObjectName("SuccessButton")
        self.btn_generate.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_generate.clicked.connect(self._generate_new_key)
        btn_box.addWidget(self.btn_generate)

        self.btn_copy = QPushButton("📋 کپی کلید")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.clicked.connect(self._copy_key)
        btn_box.addWidget(self.btn_copy)

        self.btn_save_key = QPushButton("💾 ذخیره و اعمال کلید")
        self.btn_save_key.setObjectName("PrimaryButton")
        self.btn_save_key.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save_key.clicked.connect(self._save_key)
        btn_box.addWidget(self.btn_save_key)

        key_card.add_layout(btn_box)

        desc_lbl = QLabel(
            "<b>نکته مهم:</b> کلیدهای فعال‌سازی این پروژه کاملاً رایگان هستند و هیچ هزینه‌ای ندارند. "
            "دکمه «تولید خودکار کلید» با استفاده از هش معتبر نسخه ۲.۲۴.۰ یک کلید بدون محدودیت برای شما صادر می‌کند."
        )
        desc_lbl.setStyleSheet("color: #64748b; font-size: 12px; margin-top: 8px;")
        desc_lbl.setWordWrap(True)
        key_card.add_widget(desc_lbl)

        layout.addWidget(key_card)
        layout.addStretch()

        self.load_saved_key()

    def load_saved_key(self):
        settings = load_settings()
        key = settings.get("license_key", "")
        self.txt_key.setText(key)
        self._on_key_typed(key)

    def _on_key_typed(self, text: str):
        cleaned = clean_key(text)
        if len(cleaned) == 24:
            self.lbl_formatted.setText(f"فرمت استاندارد: \u202A{format_key(cleaned)}\u202C")
        else:
            self.lbl_formatted.setText(f"طول کلید: {len(cleaned)} از ۲۴ کاراکتر")

        if verify_key(cleaned):
            self.badge_license.set_status("کلید معتبر است ✓", "success")
            self.txt_key.setStyleSheet("direction: ltr; font-family: Consolas, monospace; font-size: 15px; font-weight: bold; border-color: #10b981;")
        elif len(cleaned) == 0:
            self.badge_license.set_status("کلید خالی است", "neutral")
            self.txt_key.setStyleSheet("direction: ltr; font-family: Consolas, monospace; font-size: 15px; font-weight: bold;")
        else:
            self.badge_license.set_status("کلید نامعتبر است", "danger")
            self.txt_key.setStyleSheet("direction: ltr; font-family: Consolas, monospace; font-size: 15px; font-weight: bold; border-color: #ef4444;")


    def _generate_new_key(self):
        """تولید آنی کلید معتبر"""
        new_key = generate_key()
        self.txt_key.setText(new_key)
        self._save_key(quiet=True)
        QMessageBox.information(
            self,
            "کلید جدید صادر شد",
            f"یک کلید فعال‌سازی کاملاً معتبر برای نسخه ۲.۲۴.۰ با موفقیت تولید و در تنظیمات ذخیره شد:\n\n\u202A{format_key(new_key)}\u202C"
        )

    def _copy_key(self):
        cleaned = clean_key(self.txt_key.text())
        if cleaned:
            QApplication.clipboard().setText(cleaned)
            QMessageBox.information(self, "کپی شد", "کلید لایسنس در حافظه کلیپ‌بورد کپی شد.")

    def _save_key(self, quiet: bool = False):
        key = clean_key(self.txt_key.text())
        if not key:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا یک کلید وارد کنید.")
            return

        if not verify_key(key):
            reply = QMessageBox.question(
                self,
                "هشدار کلید نامعتبر",
                "این کلید از نظر الگوریتم نسخه ۲.۲۴.۰ نامعتبر شناخته شده است. آیا همچنان مایل به ذخیره آن هستید؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        settings = load_settings()
        settings["license_key"] = key
        save_settings(settings)
        self.license_updated.emit()

        if not quiet:
            QMessageBox.information(self, "ذخیره شد", "کلید فعال‌سازی با موفقیت ذخیره گردید.")
