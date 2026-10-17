"""
تب لاگ‌ها، ژورنال رخدادها و گزارش تشخیصی سیستم
"""

import json
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

try:
    from ..core.log_translator import translate_gate_dict, translate_log_text
    from ..core.service_manager import (
        get_diagnostic_report,
        get_forwarder_logs,
        get_watchdog_logs,
    )
    from ..core.settings_manager import get_gate_file_path, load_gate_status
    from .components import CardWidget
except (ImportError, ValueError):
    from core.log_translator import translate_gate_dict, translate_log_text
    from core.service_manager import (
        get_diagnostic_report,
        get_forwarder_logs,
        get_watchdog_logs,
    )
    from core.settings_manager import get_gate_file_path, load_gate_status
    from ui.components import CardWidget




class LogsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(12)

        # نوار ابزار بالا
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        lbl_select = QLabel("<b>منبع لاگ:</b>")
        top_bar.addWidget(lbl_select)

        self.combo_source = QComboBox()
        self.combo_source.addItem("لاگ سرویس رله و پروکسی (forwarder.log)", "forwarder")
        self.combo_source.addItem("لاگ سرویس نگهبان خودکار (watchdog.log)", "watchdog")
        self.combo_source.addItem("وضعیت زنده دروازه عبور (gate.json)", "gate")
        self.combo_source.currentIndexChanged.connect(self.refresh_logs)
        top_bar.addWidget(self.combo_source)

        top_bar.addStretch()

        self.btn_refresh = QPushButton("🔄 تازه‌سازی")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.refresh_logs)
        top_bar.addWidget(self.btn_refresh)

        self.btn_copy_report = QPushButton("📋 کپی گزارش کامل تشخیصی")
        self.btn_copy_report.setObjectName("PrimaryButton")
        self.btn_copy_report.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy_report.clicked.connect(self._copy_diagnostic_report)
        top_bar.addWidget(self.btn_copy_report)

        layout.addLayout(top_bar)

        # پنجره متنی نمایش لاگ
        self.txt_log = QPlainTextEdit()
        self.txt_log.setReadOnly(True)
        self.txt_log.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0b0f17;
                color: #5eead4;
                font-family: "Consolas", "Courier New", monospace;
                font-size: 12px;
                border: 1px solid #202b3c;
                border-radius: 8px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(self.txt_log)

        # تایمر برای بروزرسانی خودکار هر ۱۰ ثانیه در صورت باز بودن تب
        self.timer = QTimer(self)
        self.timer.setInterval(10000)
        self.timer.timeout.connect(self.refresh_logs)
        self.timer.start()

        self.refresh_logs()

    def refresh_logs(self):
        source = self.combo_source.currentData()
        if source == "forwarder":
            content = get_forwarder_logs(300)
        elif source == "watchdog":
            content = get_watchdog_logs(300)
        elif source == "gate":
            gate_data = load_gate_status()
            if gate_data:
                translated_gate = translate_gate_dict(gate_data)
                content = json.dumps(translated_gate, indent=2, ensure_ascii=False)
            else:
                content = "اطلاعات دروازه (gate.json) هنوز تشکیل نشده است یا سرویس فعال نیست."
        else:
            content = ""

        self.txt_log.setPlainText(content)

        # اسکرول به انتهای لاگ
        cursor = self.txt_log.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.txt_log.setTextCursor(cursor)

    def _copy_diagnostic_report(self):
        report = get_diagnostic_report()
        QApplication.clipboard().setText(report)
        QMessageBox.information(
            self,
            "گزارش کپی شد",
            "گزارش کامل وضعیت سیستم و لاگ‌ها در حافظه کپی شد. می‌توانید آن را برای بررسی در اختیار پشتیبانی یا توسعه‌دهنده قرار دهید."
        )
