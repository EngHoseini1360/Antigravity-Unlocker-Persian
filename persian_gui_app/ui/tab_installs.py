"""
تب مدیریت نصب‌ها و فایل‌های باینری: نمایش جزئیات نسخه‌ها، پچ تکی و افزودن مسیر دستی
"""

import os
import subprocess
import sys
from pathlib import Path
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

try:
    from ..core.detector import is_valid_install_root, scan_all_installs
    from ..core.patcher import (
        check_binary_status,
        patch_binary_file,
        unpatch_binary_file,
    )
    from ..core.settings_manager import load_settings, save_settings
    from .components import CardWidget, StatusBadge
except (ImportError, ValueError):
    from core.detector import is_valid_install_root, scan_all_installs
    from core.patcher import (
        check_binary_status,
        patch_binary_file,
        unpatch_binary_file,
    )
    from core.settings_manager import load_settings, save_settings
    from ui.components import CardWidget, StatusBadge



class InstallCard(QFrame):
    """کارت نمایش یک نصب Antigravity و باینری‌های داخل آن"""
    action_completed = pyqtSignal()

    def __init__(self, install_data: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("CardFrame")
        self.install_data = install_data

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # ردیف هدر
        header = QHBoxLayout()
        header.setSpacing(8)

        icon = "💻" if "ide" in install_data["label"].lower() else "🚀"
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 20px;")
        header.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_lbl = QLabel(install_data["label"])
        title_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8;")
        title_box.addWidget(title_lbl)

        path_lbl = QLabel(install_data["path"])
        path_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        title_box.addWidget(path_lbl)

        header.addLayout(title_box)
        header.addStretch()

        btn_open = QPushButton("باز کردن پوشه")
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.clicked.connect(self._open_in_explorer)
        header.addWidget(btn_open)

        layout.addLayout(header)

        # خط جداکننده
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #222f3e; max-height: 1px;")
        layout.addWidget(sep)

        # باینری‌ها
        binaries = install_data.get("binaries", [])
        if not binaries:
            no_bin = QLabel("هیچ باینری قابل پچ در این پوشه شناسایی نشد.")
            no_bin.setStyleSheet("color: #ef4444; font-size: 12px;")
            layout.addWidget(no_bin)
        else:
            for b_path in binaries:
                layout.addWidget(self._build_binary_row(b_path))

    def _build_binary_row(self, b_path: str) -> QWidget:
        row = QFrame()
        row.setStyleSheet("background-color: #0d131d; border-radius: 8px; padding: 6px;")
        r_layout = QHBoxLayout(row)
        r_layout.setContentsMargins(10, 8, 10, 8)
        r_layout.setSpacing(10)

        p = Path(b_path)
        stat = check_binary_status(b_path)

        info_box = QVBoxLayout()
        info_box.setSpacing(2)

        name_lbl = QLabel(f"<b>{p.name}</b>")
        info_box.addWidget(name_lbl)

        size_text = f"حجم: {stat.get('size_mb', 0)} مگابایت | {p.parent}"
        sub_lbl = QLabel(size_text)
        sub_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        info_box.addWidget(sub_lbl)

        r_layout.addLayout(info_box)
        r_layout.addStretch()

        # وضعیت پچ
        status_map = {
            "patched": ("پچ شده (رفع تحریم)", "success"),
            "unpatched": ("پچ نشده (محدود به ریجن)", "danger"),
            "partial": ("پچ ناقص", "warning"),
            "locked": ("قفل شده توسط پروسه", "warning"),
            "missing": ("فایل یافت نشد", "neutral"),
            "unknown": ("امضا ناشناخته", "neutral"),
        }
        badge_text, badge_type = status_map.get(stat["status"], ("نامشخص", "neutral"))
        badge = StatusBadge(badge_text, badge_type)
        r_layout.addWidget(badge)

        # دکمه پچ
        btn_patch = QPushButton("پچ")
        btn_patch.setObjectName("SuccessButton")
        btn_patch.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_patch.setEnabled(stat["status"] in ["unpatched", "partial", "locked"])
        btn_patch.clicked.connect(lambda: self._patch_binary(b_path))
        r_layout.addWidget(btn_patch)

        # دکمه آنپچ
        btn_unpatch = QPushButton("بازگردانی")
        btn_unpatch.setObjectName("DangerButton")
        btn_unpatch.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_unpatch.setEnabled(stat["status"] in ["patched", "partial"])
        btn_unpatch.clicked.connect(lambda: self._unpatch_binary(b_path))
        r_layout.addWidget(btn_unpatch)

        return row

    def _open_in_explorer(self):
        path = self.install_data["path"]
        if os.path.exists(path):
            if hasattr(os, "startfile"):
                os.startfile(path)
            elif sys.platform == "darwin":
                try:
                    subprocess.Popen(["open", path])
                except Exception:
                    pass
            else:
                try:
                    subprocess.Popen(["xdg-open", path])
                except Exception:
                    pass

    def _patch_binary(self, b_path: str):
        ok, msg = patch_binary_file(b_path)
        if ok:
            QMessageBox.information(self, "موفقیت", msg)
        else:
            QMessageBox.warning(self, "خطا", msg)
        self.action_completed.emit()

    def _unpatch_binary(self, b_path: str):
        ok, msg = unpatch_binary_file(b_path)
        if ok:
            QMessageBox.information(self, "موفقیت", msg)
        else:
            QMessageBox.warning(self, "خطا", msg)
        self.action_completed.emit()


class InstallsTab(QWidget):
    installs_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(12)

        # نوار ابزار بالا
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        title_lbl = QLabel("لیست نسخه‌های شناسایی شده Antigravity در سیستم")
        title_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")
        top_bar.addWidget(title_lbl)
        top_bar.addStretch()

        btn_add_folder = QPushButton("📁 افزودن پوشه نصب")
        btn_add_folder.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_folder.clicked.connect(self._add_manual_folder)
        top_bar.addWidget(btn_add_folder)

        btn_add_file = QPushButton("📄 افزودن مستقیم فایل (language_server)")
        btn_add_file.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_file.clicked.connect(self._add_manual_file)
        top_bar.addWidget(btn_add_file)

        btn_rescan = QPushButton("🔄 اسکن دوباره سیستم")
        btn_rescan.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_rescan.clicked.connect(self.reload_installs)
        top_bar.addWidget(btn_rescan)

        layout.addLayout(top_bar)

        # ناحیه اسکرول برای کارت‌های نصب
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(14)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll.setWidget(self.cards_container)
        layout.addWidget(self.scroll)

        self.reload_installs()

    def reload_installs(self):
        """اسکن و بارگذاری مجدد لیست نصب‌ها"""
        # پاک‌سازی ویجت‌های قبلی
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        installs = scan_all_installs()
        if not installs:
            empty_card = CardWidget("نصبی یافت نشد", "هیچ پوشه‌ای از Antigravity در مسیرهای استاندارد پیدا نشد.", "⚠️")
            lbl = QLabel(
                "اگر Antigravity یا Language Server را در پوشه دیگری (مانند ترموکس، پوشه دانلود یا دایرکتوری خانگی) قرار داده‌اید،\n"
                "می‌توانید با دکمه «📁 افزودن پوشه نصب» یا «📄 افزودن مستقیم فایل» مسیر آن را مشخص نمایید."
            )
            lbl.setStyleSheet("color: #94a3b8; font-size: 13px;")
            empty_card.add_widget(lbl)
            self.cards_layout.addWidget(empty_card)
        else:
            for inst in installs:
                card = InstallCard(inst)
                card.action_completed.connect(self._on_card_action_completed)
                self.cards_layout.addWidget(card)

    def _on_card_action_completed(self):
        self.reload_installs()
        self.installs_changed.emit()

    def _add_manual_folder(self):
        """انتخاب پوشه سفارشی توسط کاربر"""
        folder = QFileDialog.getExistingDirectory(self, "انتخاب پوشه نصب Antigravity")
        if not folder:
            return

        folder_path = Path(folder)
        if not is_valid_install_root(folder_path):
            reply = QMessageBox.question(
                self,
                "تأیید مسیر",
                "در این پوشه فایل اجرایی با نام استاندارد پیدا نشد. آیا همچنان مایلید این مسیر به لیست اضافه شود؟",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        settings = load_settings()
        manual_paths = settings.get("manual_paths", [])
        if str(folder_path) not in manual_paths:
            manual_paths.append(str(folder_path))
            settings["manual_paths"] = manual_paths
            save_settings(settings)
            QMessageBox.information(self, "ثبت شد", "مسیر مورد نظر به لیست اسکن افزوده شد.")
            self.reload_installs()
            self.installs_changed.emit()
        else:
            QMessageBox.information(self, "موجود است", "این مسیر از قبل در لیست وجود دارد.")

    def _add_manual_file(self):
        """انتخاب مستقیم فایل باینری (مانند language_server یا agy) توسط کاربر"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "انتخاب مستقیم فایل باینری Antigravity (language_server یا agy)",
            "",
            "تمام فایل‌ها (*);;باینری‌های اجرایی (language_server* agy* *.exe)"
        )
        if not file_path:
            return

        fp = Path(file_path)
        settings = load_settings()
        manual_paths = settings.get("manual_paths", [])
        if str(fp) not in manual_paths:
            manual_paths.append(str(fp))
            settings["manual_paths"] = manual_paths
            save_settings(settings)
            QMessageBox.information(self, "ثبت شد", f"فایل باینری {fp.name} به لیست اضافه شد.")
            self.reload_installs()
            self.installs_changed.emit()
        else:
            QMessageBox.information(self, "موجود است", "این فایل از قبل در لیست وجود دارد.")
