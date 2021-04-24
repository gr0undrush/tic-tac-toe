import sys

from data.const import *
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton
from PyQt6.QtCore import pyqtSlot

PL_SMB = 'X'


class Ui(QWidget):
    def __init__(self):
        self.app = QApplication([])

        super().__init__()

        self.field = []
        self.layout = QGridLayout()
        self.gui_init()

    def gui_init(self):
        self.setWindowTitle(f'{APP_NAME} {APP_VERSION}')
        for x in range(H_SIZE):
            row = []
            for y in range(V_SIZE):
                btn = QPushButton(text=f'')
                btn.setFixedWidth(BUTTON_WIDTH)
                btn.setFixedHeight(BUTTIN_HEIGHT)
                btn.clicked.connect(self.on_click)
                row.append(btn)
                self.layout.addWidget(btn, x, y)

            self.field.append(row)

        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        if self.sender().text() == '':
            self.sender().setText(PL_SMB)

    def start(self):
        self.show()
        sys.exit(self.app.exec())
