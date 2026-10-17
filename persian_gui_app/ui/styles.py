"""
استایل‌های مدرن و تم دارک Fluent Windows 11 برای رابط کاربری فارسی
با پشتیبانی کامل از چینش راست‌به‌چپ (RTL) و تایپوگرافی تمیز
"""

MAIN_STYLESHEET = """
* {
    font-family: "Segoe UI", "Tahoma", "Vazirmatn", "Shabnam", sans-serif;
    outline: none;
}

QMainWindow, QDialog {
    background-color: #0b0f17;
    color: #e6edf3;
}

QWidget {
    color: #e6edf3;
    font-size: 13px;
}

/* کارت‌های پنل و کانتینرها */
QFrame#CardFrame {
    background-color: #131b26;
    border: 1px solid #222f3e;
    border-radius: 12px;
}

QFrame#CardFrame:hover {
    border: 1px solid #3b82f6;
}

QFrame#StatusBannerCard {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1a2332, stop:1 #131b26);
    border: 1px solid #2d3e53;
    border-radius: 14px;
}

/* تب‌بار مدرن و افقی */
QTabWidget::pane {
    border: none;
    background-color: transparent;
}

QTabBar::tab {
    background-color: #161f2e;
    color: #94a3b8;
    padding: 10px 22px;
    margin-left: 6px;
    margin-right: 6px;
    margin-bottom: 8px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #202b3c;
}

QTabBar::tab:selected {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #3b82f6;
}

QTabBar::tab:hover:!selected {
    background-color: #1e293b;
    color: #cbd5e1;
}

/* دکمه‌ها */
QPushButton {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #475569;
}

QPushButton:pressed {
    background-color: #0f172a;
}

QPushButton:disabled {
    background-color: #0f172a;
    color: #475569;
    border-color: #1e293b;
}

/* دکمه‌های پرایمری (اصلی و برجسته) */
QPushButton#PrimaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
    color: #ffffff;
    border: 1px solid #3b82f6;
    border-radius: 10px;
    font-weight: bold;
    font-size: 14px;
    padding: 12px 24px;
}

QPushButton#PrimaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b82f6, stop:1 #2563eb);
    border-color: #60a5fa;
}

QPushButton#PrimaryButton:pressed {
    background: #1e40af;
}

/* دکمه موفقیت (سبز) */
QPushButton#SuccessButton {
    background-color: #10b981;
    color: #ffffff;
    border: 1px solid #059669;
}

QPushButton#SuccessButton:hover {
    background-color: #059669;
}

/* دکمه خطر یا بازگردانی (قرمز) */
QPushButton#DangerButton {
    background-color: #ef4444;
    color: #ffffff;
    border: 1px solid #dc2626;
}

QPushButton#DangerButton:hover {
    background-color: #dc2626;
}

/* فیلدهای متنی و ورودی‌ها */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #0d131d;
    color: #f1f5f9;
    border: 1px solid #202b3c;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #2563eb;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3b82f6;
    background-color: #101723;
}

/* جدول‌ها و لیست‌ها */
QTableWidget {
    background-color: #101722;
    gridline-color: #1e293b;
    border: 1px solid #202b3c;
    border-radius: 8px;
    color: #f1f5f9;
    selection-background-color: #1e3a5f;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #16202e;
    color: #94a3b8;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #202b3c;
    font-weight: bold;
}

/* اسکرول بار باریک و زیبا */
QScrollBar:vertical {
    border: none;
    background-color: #0b0f17;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #243144;
    min-height: 25px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3b82f6;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background-color: #0b0f17;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #243144;
    min-width: 25px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #3b82f6;
}

/* برچسب‌ها و عناوین */
QLabel {
    color: #e2e8f0;
}

QLabel#HeaderTitle {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
}

QLabel#SubTitle {
    font-size: 12px;
    color: #94a3b8;
}

QLabel#CardTitle {
    font-size: 15px;
    font-weight: bold;
    color: #38bdf8;
}

/* تول‌تیپ */
QToolTip {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
}
"""
