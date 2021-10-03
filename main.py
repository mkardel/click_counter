"""
Count left- and right mouse clicks.
Matthias Kardel 2021-09-30
"""

import sys
import typing

from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtCore import QEvent, QObject, Qt


if typing.TYPE_CHECKING:
    from typing import Type


MouseButtons = {
    Qt.LeftButton: "Left",
    Qt.RightButton: "Right",
    Qt.MiddleButton: "Middle",
    Qt.XButton1: "Mouse4",
    Qt.XButton2: "Mouse5"
}


class ClickCounter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        click_me_button = QPushButton("Click here")
        click_me_button.installEventFilter(self)

        self.click_counter = {}

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)

        counter_widget_box = QWidget(self)
        counter_layout = QHBoxLayout(counter_widget_box)

        self.click_labels = {}
        for button_id, _ in MouseButtons.items():
            self.click_labels[button_id] = QLabel(counter_widget_box)
            counter_layout.addWidget(self.click_labels[button_id])

        layout = QVBoxLayout()
        layout.addWidget(click_me_button)
        layout.addWidget(reset_button)
        layout.addWidget(counter_widget_box)

        self.setWindowTitle("Click Counter")
        self.setLayout(layout)
        self.reset()

    def update(self):
        for button_id, qlabel in self.click_labels.items():
            qlabel.setText(f"{MouseButtons[button_id]}: {self.click_counter[button_id]}")

    def reset(self):
        for click_id, label in MouseButtons.items():
            self.click_counter[click_id] = 0
        self.update()

    def eventFilter(self, obj: 'QObject', event: 'Type[QEvent]') -> bool:
        if event.type() == QEvent.MouseButtonRelease and event.button() in MouseButtons.keys():
            self.click_counter[event.button()] += 1
            self.update()
        return False


def run():
    app = QApplication(sys.argv)
    w = ClickCounter()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
