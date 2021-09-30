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


class ClickCounter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        click_me_button = QPushButton("Click here")
        click_me_button.installEventFilter(self)

        self.left_click_counter = 0
        self.right_click_counter = 0

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)

        counter_widget_box = QWidget(self)
        counter_layout = QHBoxLayout(counter_widget_box)

        self.left_click_label = QLabel(counter_widget_box)
        self.right_click_label = QLabel(counter_widget_box)
        counter_layout.addWidget(self.left_click_label)
        counter_layout.addWidget(self.right_click_label)
        self.update_left()
        self.update_right()

        layout = QVBoxLayout()
        layout.addWidget(click_me_button)
        layout.addWidget(reset_button)
        layout.addWidget(counter_widget_box)

        self.setWindowTitle("Click Counter")
        self.setLayout(layout)

    def update_left(self):
        self.left_click_label.setText("Left: {}".format(self.left_click_counter))

    def update_right(self):
        self.right_click_label.setText("Right: {}".format(self.right_click_counter))

    def update_all(self):
        self.update_right()
        self.update_left()

    def reset(self):
        self.left_click_counter = 0
        self.right_click_counter = 0
        self.update_all()

    def eventFilter(self, obj: 'QObject', event: 'Type[QEvent]') -> bool:
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self.left_click_counter += 1
                self.update_left()
            elif event.button() == Qt.RightButton:
                self.right_click_counter += 1
                self.update_right()
        return False


def run():
    app = QApplication(sys.argv)
    w = ClickCounter()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
