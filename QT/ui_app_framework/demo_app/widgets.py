from __future__ import annotations

import json

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MetricCard(QFrame):
    def __init__(self, label: str, accent: str):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(
            f"QFrame {{ border: 1px solid #d6dbe4; border-left: 4px solid {accent}; background: #fbfcfe; }}"
        )

        self.label = QLabel(label)
        self.value = QLabel("0")
        self.value.setStyleSheet("font-size: 26px; font-weight: 600;")
        self.caption = QLabel("Live")
        self.caption.setStyleSheet("color: #64748b;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        layout.addWidget(self.caption)

    def set_value(self, value: str, caption: str = "Live"):
        self.value.setText(value)
        self.caption.setText(caption)


class StatusDistributionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._items: list[tuple[str, int, QColor]] = []
        self.setMinimumHeight(180)

    def set_items(self, items: list[tuple[str, int, str]]):
        self._items = [(label, value, QColor(color)) for label, value, color in items]
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#ffffff"))

        if not self._items:
            painter.setPen(QColor("#94a3b8"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No runtime data yet")
            return

        max_value = max(1, max(value for _, value, _ in self._items))
        left = 18
        top = 18
        row_height = 28
        bar_max_width = max(120, self.width() - 180)

        for index, (label, value, color) in enumerate(self._items):
            y = top + index * row_height
            painter.setPen(QColor("#0f172a"))
            painter.drawText(left, y + 15, label)

            bar_x = left + 110
            bar_y = y + 4
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#e5e7eb"))
            painter.drawRoundedRect(QRectF(bar_x, bar_y, bar_max_width, 14), 4, 4)

            painter.setBrush(color)
            width = bar_max_width * (value / max_value)
            painter.drawRoundedRect(QRectF(bar_x, bar_y, width, 14), 4, 4)

            painter.setPen(QColor("#334155"))
            painter.drawText(bar_x + bar_max_width + 10, y + 15, str(value))


class JsonSnapshotView(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.title = QLabel("Runtime Snapshot JSON")
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("Snapshot preview will appear here...")

        self.refresh_button = QPushButton("Refresh Preview")
        self.export_button = QPushButton("Export JSON")
        self.path_label = QLabel("No export yet")
        self.path_label.setStyleSheet("color: #64748b;")

        actions = QHBoxLayout()
        actions.addWidget(self.refresh_button)
        actions.addWidget(self.export_button)
        actions.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addLayout(actions)
        layout.addWidget(self.preview)
        layout.addWidget(self.path_label)

    def set_snapshot(self, payload: dict):
        self.preview.setPlainText(json.dumps(payload, indent=2, sort_keys=True))

    def set_export_path(self, path: str):
        self.path_label.setText(path)
