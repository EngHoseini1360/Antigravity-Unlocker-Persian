"""
پنجره اصلی برنامه Antigravity Unlocker به زبان فارسی
"""

import os
from pathlib import Path
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

try:
    from .core.service_manager import is_admin, run_as_admin
    from .ui.styles import MAIN_STYLESHEET
    from .ui.tab_dashboard import DashboardTab
    from .ui.tab_guide import GuideTab
    from .ui.tab_installs import InstallsTab
    from .ui.tab_license import LicenseTab
    from .ui.tab_logs import LogsTab
    from .ui.tab_network import NetworkTab
except (ImportError, ValueError):
    from core.service_manager import is_admin, run_as_admin
    from ui.styles import MAIN_STYLESHEET
    from ui.tab_dashboard import DashboardTab
    from ui.tab_guide import GuideTab
    from ui.tab_installs import InstallsTab
    from ui.tab_license import LicenseTab
    from ui.tab_logs import LogsTab
    from ui.tab_network import NetworkTab



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antigravity Unlocker - رابط کاربری فارسی | برنامه‌نویس: AliasgharHoseini")
        self.resize(1000, 720)
        self.setMinimumSize(850, 600)

        # اعمال استایل کلی
        self.setStyleSheet(MAIN_STYLESHEET)

        # تنظیم آیکون پنجره
        self._set_app_icon()

        # ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(16, 14, 16, 12)
        self.main_layout.setSpacing(12)

        # نوار بالای پنجره (Header Bar)
        self._build_top_bar()

        # تب‌های برنامه
        self._build_tabs()

        # نوار وضعیت پایینی
        self._build_status_bar()

    def _set_app_icon(self):
        """تنظیم آیکون برنامه از فایل icon.ico پروژه"""
        candidates = [
            Path(__file__).parent.parent / "icon.ico",
            Path(__file__).parent / "icon.ico",
            Path(r"H:\Project\Antigravity-2.24.0\Antigravity-2.24.0\icon.ico"),
        ]
        for p in candidates:
            if p.exists():
                self.setWindowIcon(QIcon(str(p)))
                break

    def _build_top_bar(self):
        """ساخت نوار سربرگ بالای پنجره با نام برنامه و دکمه دسترسی مدیر"""
        top_frame = QFrame()
        top_frame.setStyleSheet("""
            QFrame {
                background-color: #131b26;
                border: 1px solid #202b3c;
                border-radius: 12px;
                padding: 4px 12px;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(12, 8, 12, 8)
        top_layout.setSpacing(12)

        # لوگو و عنوان
        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(2)

        title_lbl = QLabel("Antigravity Unlocker — نسخه فارسی")
        title_lbl.setStyleSheet("font-size: 17px; font-weight: bold; color: #38bdf8;")
        brand_layout.addWidget(title_lbl)

        sub_lbl = QLabel("ابزار هوشمند دور زدن تحریم و رفع ارور 400 برای Antigravity و Antigravity IDE")
        sub_lbl.setStyleSheet("font-size: 12px; color: #94a3b8;")
        brand_layout.addWidget(sub_lbl)

        top_layout.addLayout(brand_layout)
        top_layout.addStretch()

        # نشان برنامه‌نویس
        dev_lbl = QLabel("👨‍💻 برنامه‌نویس: AliasgharHoseini")
        dev_lbl.setStyleSheet("""
            background-color: #1a2332;
            color: #38bdf8;
            font-weight: bold;
            font-size: 12px;
            padding: 6px 14px;
            border-radius: 8px;
            border: 1px solid #2d3e53;
        """)
        top_layout.addWidget(dev_lbl)

        # دکمه بررسی دسترسی ادمین
        if not is_admin():
            self.btn_admin = QPushButton("🛡️ اجرا با دسترسی Administrator")
            self.btn_admin.setToolTip("برای فعال‌سازی کامل قوانین DNS NRPT ویندوز به دسترسی مدیر نیاز است.")
            self.btn_admin.setStyleSheet("""
                QPushButton {
                    background-color: #f59e0b;
                    color: #000000;
                    font-weight: bold;
                    border: 1px solid #d97706;
                    border-radius: 8px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #fbbf24;
                }
            """)
            self.btn_admin.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_admin.clicked.connect(self._restart_as_admin)
            top_layout.addWidget(self.btn_admin)
        else:
            admin_lbl = QLabel("🛡️ دسترسی ادمین فعال است ✓")
            admin_lbl.setStyleSheet("color: #10b981; font-weight: bold; font-size: 13px; padding: 6px 12px;")
            top_layout.addWidget(admin_lbl)

        self.main_layout.addWidget(top_frame)

    def _build_tabs(self):
        """ساخت تب‌های اصلی و اتصال رویدادهای میان تب‌ها"""
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.tab_dashboard = DashboardTab(self)
        self.tab_installs = InstallsTab(self)
        self.tab_network = NetworkTab(self)
        self.tab_license = LicenseTab(self)
        self.tab_logs = LogsTab(self)
        self.tab_guide = GuideTab(self)

        self.tabs.addTab(self.tab_dashboard, "📊  داشبورد وضعیت")
        self.tabs.addTab(self.tab_installs, "📁  مدیریت نسخه‌ها و فایل‌ها")
        self.tabs.addTab(self.tab_network, "🌐  تنظیمات شبکه و پروکسی")
        self.tabs.addTab(self.tab_license, "🔑  کلید فعال‌سازی")
        self.tabs.addTab(self.tab_logs, "📜  لاگ‌ها و ژورنال")
        self.tabs.addTab(self.tab_guide, "💡  راهنمای جامع")

        # اتصال سیگنال‌های بین تب‌ها
        self.tab_dashboard.status_changed.connect(self.tab_installs.reload_installs)
        self.tab_license.license_updated.connect(self.tab_dashboard.update_license_only)
        self.tab_installs.installs_changed.connect(self.tab_dashboard.refresh_status)


        self.main_layout.addWidget(self.tabs)

    def _build_status_bar(self):
        """نوار وضعیت در پایین پنجره"""
        self.status = QStatusBar()
        self.status.setStyleSheet("color: #94a3b8; font-size: 12px; background-color: #0b0f17;")
        self.setStatusBar(self.status)
        self.status.showMessage("آماده به کار — نسخه ۲.۲۴.۰ | برنامه‌نویس: AliasgharHoseini")


    def _restart_as_admin(self):
        """درخواست اجرای برنامه با دسترسی مدیر"""
        run_as_admin()
