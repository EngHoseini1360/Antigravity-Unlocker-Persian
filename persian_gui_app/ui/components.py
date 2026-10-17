"""
ویجت‌های سفارشی و مدرن رابط کاربری شامل کلیدهای تاگل انیمیشنی، کارت‌ها و نشانگرهای وضعیت
"""

from PyQt6.QtCore import (
    QPropertyAnimation,
    QRect,
    QRectF,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class ToggleSwitch(QCheckBox):
    """
    سوئیچ تاگل مدرن (Toggle Switch) مشابه کنترل‌های ویندوز ۱۱ و iOS
    """
    def __init__(self, parent=None, width=52, height=28, bg_color="#202b3c", active_color="#2563eb"):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bg_color = QColor(bg_color)
        self._active_color = QColor(active_color)
        self._circle_color = QColor("#ffffff")
        self._position = 3.0

        self._anim = QPropertyAnimation(self, b"position")
        self._anim.setDuration(160)

        self.stateChanged.connect(self._on_state_changed)

    def _get_position(self):
        return self._position

    def _set_position(self, pos):
        self._position = pos
        self.update()

    position = pyqtProperty(float, _get_position, _set_position)

    def _on_state_changed(self, state):
        self._anim.stop()
        if self.isChecked():
            self._anim.setEndValue(self.width() - 25.0)
        else:
            self._anim.setEndValue(3.0)
        self._anim.start()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._position = (self.width() - 25.0) if checked else 3.0
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # رسم پس‌زمینه کپسولی
        bg = self._active_color if self.isChecked() else self._bg_color
        p.setBrush(QBrush(bg))
        p.setPen(Qt.PenStyle.NoPen)
        r = self.rect()
        radius = r.height() / 2.0
        p.drawRoundedRect(QRectF(r), radius, radius)

        # رسم دایره سوئیچ
        p.setBrush(QBrush(self._circle_color))
        circle_diam = r.height() - 6.0
        p.drawEllipse(QRectF(self._position, 3.0, circle_diam, circle_diam))
        p.end()


class CardWidget(QFrame):
    """
    کارت مدرن محفظه عناصر با حاشیه نرم، عنوان و آیکون
    """
    def __init__(self, title: str = "", subtitle: str = "", icon: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("CardFrame")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 16, 18, 16)
        self.layout.setSpacing(10)

        if title or icon:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(8)

            if icon:
                icon_lbl = QLabel(icon)
                icon_lbl.setStyleSheet("font-size: 18px;")
                header_layout.addWidget(icon_lbl)

            title_box = QVBoxLayout()
            title_box.setSpacing(2)

            title_lbl = QLabel(title)
            title_lbl.setObjectName("CardTitle")
            title_box.addWidget(title_lbl)

            if subtitle:
                sub_lbl = QLabel(subtitle)
                sub_lbl.setObjectName("SubTitle")
                title_box.addWidget(sub_lbl)

            header_layout.addLayout(title_box)
            header_layout.addStretch()
            self.layout.addLayout(header_layout)

    def add_widget(self, widget: QWidget):
        self.layout.addWidget(widget)

    def add_layout(self, layout):
        self.layout.addLayout(layout)


class StatusBadge(QFrame):
    """
    نشانگر وضعیت کپسولی رنگی با چراغ وضعیت و متن
    """
    def __init__(self, text: str = "غیرفعال", status_type: str = "danger", parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 4, 10, 4)
        self.layout.setSpacing(6)

        self.dot = QLabel("●")
        self.label = QLabel(text)
        self.label.setStyleSheet("font-weight: bold; font-size: 12px;")

        self.layout.addWidget(self.dot)
        self.layout.addWidget(self.label)

        self.set_status(text, status_type)

    def set_status(self, text: str, status_type: str):
        self.label.setText(text)
        colors = {
            "success": ("#10b981", "#064e3b", "#10b981"),
            "danger": ("#ef4444", "#450a0a", "#ef4444"),
            "warning": ("#f59e0b", "#451a03", "#f59e0b"),
            "info": ("#3b82f6", "#172554", "#3b82f6"),
            "neutral": ("#94a3b8", "#1e293b", "#94a3b8"),
        }
        text_color, bg_color, dot_color = colors.get(status_type, colors["neutral"])
        self.dot.setStyleSheet(f"color: {dot_color}; font-size: 10px;")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {text_color};
                border-radius: 12px;
            }}
            QLabel {{
                color: {text_color};
            }}
        """)


class SwitchRow(QWidget):
    """
    ردیف یکپارچه شامل عنوان، توضیحات، و سوئیچ تاگل
    """
    toggled = pyqtSignal(bool)

    def __init__(self, title: str, description: str = "", initial_state: bool = False, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-weight: 600; font-size: 14px; color: #f8fafc;")
        text_layout.addWidget(title_lbl)

        if description:
            desc_lbl = QLabel(description)
            desc_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
            desc_lbl.setWordWrap(True)
            text_layout.addWidget(desc_lbl)

        layout.addLayout(text_layout)
        layout.addStretch()

        self.switch = ToggleSwitch()
        self.switch.setChecked(initial_state)
        self.switch.stateChanged.connect(lambda s: self.toggled.emit(self.switch.isChecked()))
        layout.addWidget(self.switch)

    def isChecked(self) -> bool:
        return self.switch.isChecked()

    def setChecked(self, checked: bool):
        self.switch.setChecked(checked)
