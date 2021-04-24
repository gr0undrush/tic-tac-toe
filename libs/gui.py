import sys
import logging
import random

from data.const import *
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIcon

logger = logging.getLogger(__name__)

HUM_SMB = 'X'
II_SMB = '0'


class Ui(QWidget):
    def __init__(self):

        logger.debug('Ui class initializing')

        self.eog = False
        self.app = QApplication([])

        super().__init__()

        self.field = []
        self.layout = QGridLayout()
        self.gui_init()

    def gui_init(self):
        logger.debug('GUI initialization')
        self.setWindowTitle(f'{APP_NAME} {APP_VERSION}')
        self.setWindowIcon(QIcon('media/icon.png'))
        for x in range(SIZE):
            row = []
            for y in range(SIZE):
                btn = QPushButton(text=f'')
                btn.setFixedWidth(BUTTON_WIDTH)
                btn.setFixedHeight(BUTTON_HEIGHT)
                btn.setAccessibleName(f'{x}/{y}')
                btn.setStyleSheet(REGULAR)

                btn.clicked.connect(self.on_click)
                row.append(btn)

                self.layout.addWidget(btn, x, y)

            self.field.append(row)

        self.setLayout(self.layout)
        logger.debug('GUI initialized')

    @pyqtSlot()
    def on_click(self):
        if self.eog:
            logger.debug('Performing field reset')
            self.eog = False

            for x in range(SIZE):
                for y in range(SIZE):
                    self.field[x][y].setText('')
                    self.field[x][y].setStyleSheet(REGULAR)

            return

        if self.sender().text() == '':
            self.sender().setText(HUM_SMB)
        else:
            return

        self.check_win()

        if not self.eog:
            self.move_it()

    def move_it(self):
        logger.debug('Performing move')

        self.check_win()

        if self.check_pairs(me=True):
            logger.debug('Used my pair rule')
            pass
        elif self.check_pairs(me=False):
            logger.debug('Used enemy pair rule')
            pass
        elif self.check_cc():
            pass
        else:
            logger.debug('Used set any rule')
            self.set_any()

        logger.debug('Checking winning combinations')
        self.check_win()

    def check_win(self):
        for x in range(SIZE):
            if self.field[0][x].text() == self.field[1][x].text() == self.field[2][x].text() != '':

                if self.field[0][x].text() == HUM_SMB:
                    logger.debug('Human won')
                    style = WIN
                else:
                    logger.debug('UI won')
                    style = LOOSE

                self.field[0][x].setStyleSheet(style)
                self.field[1][x].setStyleSheet(style)
                self.field[2][x].setStyleSheet(style)

                self.eog = True

            if self.field[x][0].text() == self.field[x][1].text() == self.field[x][2].text() != '':

                if self.field[0][x].text() == HUM_SMB:
                    logger.debug('Human won')
                    style = WIN
                else:
                    logger.debug('UI won')
                    style = LOOSE

                self.field[x][0].setStyleSheet(style)
                self.field[x][1].setStyleSheet(style)
                self.field[x][2].setStyleSheet(style)

                self.eog = True

        if self.field[0][0].text() == self.field[1][1].text() == self.field[2][2].text() != '':

            if self.field[0][0].text() == HUM_SMB:
                logger.debug('Human won')
                style = WIN
            else:
                logger.debug('UI won')
                style = LOOSE

            self.field[0][0].setStyleSheet(style)
            self.field[1][1].setStyleSheet(style)
            self.field[2][2].setStyleSheet(style)

            self.eog = True

        if self.field[0][2].text() == self.field[1][1].text() == self.field[2][0].text() != '':

            if self.field[0][2].text() == HUM_SMB:
                logger.debug('Human won')
                style = WIN
            else:
                logger.debug('UI won')
                style = LOOSE

            self.field[0][2].setStyleSheet(style)
            self.field[1][1].setStyleSheet(style)
            self.field[2][0].setStyleSheet(style)

            self.eog = True

    def check_pairs(self, me: bool):

        if me:
            symbol = II_SMB
        else:
            symbol = HUM_SMB

        for x in range(SIZE):
            for y in range(SIZE):

                logger.debug(f'Processing coordinates: {x} {y}')

                logger.debug(f'Checking: ({x}-{y}) == ({(1 + x) % SIZE}-{y}) == {symbol}')
                if self.field[x][y].text() == self.field[(1 + x) % SIZE][y].text() == symbol and \
                        self.field[(2 + x) % SIZE][y].text() == '':
                    self.field[(2 + x) % SIZE][y].setText(II_SMB)

                    logger.debug(f'Pair rule: ({x}-{y}) == ({(1 + x) % SIZE}-{y}) == {symbol}')

                    return True

                logger.debug(f'Checking: ({y}-{x}) == ({y}-{(1 + x) % SIZE}) == {symbol}')
                if self.field[y][x].text() == self.field[y][(1 + x) % SIZE].text() == symbol and \
                        self.field[y][(2 + x) % SIZE].text() == '':
                    self.field[y][(2 + x) % SIZE].setText(II_SMB)

                    logger.debug(f'Pair rule: ({y}-{x}) == ({y}-{(1 + x) % SIZE}) == {symbol}')

                    return True

            logger.debug(f'Checking: ({x}-{x}) == ({(1 + x) % SIZE}-{(1 + x) % SIZE}) == {symbol}')
            if self.field[x][x].text() == self.field[(1 + x) % SIZE][(1 + x) % SIZE].text() == symbol and \
                    self.field[(2 + x) % SIZE][(2 + x) % SIZE].text() == '':
                self.field[(2 + x) % SIZE][(2 + x) % SIZE].setText(II_SMB)

                logger.debug(f'Pair rule: ({x}-{x}) == ({(1 + x) % SIZE}-{(1 + x) % SIZE}) == {symbol}')

                return True

            logger.debug(f'Checking: ({x}-{(2 - x) % SIZE}) == ({(1 + x) % SIZE}-{(1 - x) % SIZE}) == {symbol}')
            if self.field[x][(2 - x) % SIZE].text() == self.field[(1 + x) % SIZE][(1 - x) % SIZE].text() == symbol and \
                    self.field[(2 + x) % SIZE][(- x) % SIZE].text() == '':
                self.field[(2 + x) % SIZE][(- x) % SIZE].setText(II_SMB)

                logger.debug(f'Pair rule: ({x}-{(2 - x) % SIZE}) == ({(1 + x) % SIZE}-{(1 - x) % SIZE}) == {symbol}')

                return True

        return False

    def check_cc(self):
        if self.field[1][1].text() == '':
            self.field[1][1].setText(II_SMB)
            logger.debug('Used center rule')
            return True
        elif self.field[1][1].text() == II_SMB and (
                self.field[0][0].text() == self.field[2][2].text() == HUM_SMB or
                self.field[0][2].text() == self.field[2][0].text() == HUM_SMB):
            logger.debug('XOX diagonal detected, making side move')
            if self.field[0][1].text() == '':
                self.field[0][1].setText(II_SMB)
                return True

            elif self.field[1][2].text() == '':
                self.field[1][2].setText(II_SMB)
                return True

            elif self.field[1][0].text() == '':
                self.field[1][0].setText(II_SMB)
                return True

            elif self.field[2][1].text() == '':
                self.field[2][1].setText(II_SMB)
                return True

        if self.field[0][0].text() == '':
            self.field[0][0].setText(II_SMB)
            logger.debug('Used corner rule')
            return True

        if self.field[2][2].text() == '':
            self.field[2][2].setText(II_SMB)
            logger.debug('Used corner rule')
            return True

        if self.field[0][2].text() == '':
            self.field[0][2].setText(II_SMB)
            logger.debug('Used corner rule')
            return True

        if self.field[2][0].text() == '':
            self.field[2][0].setText(II_SMB)
            logger.debug('Used corner rule')
            return True

        return False

    def set_any(self):
        for x in range(SIZE - 1):
            for y in range(SIZE - 1):
                if self.field[x][y].text() == '':
                    self.field[x][y].setText(II_SMB)

                    return

        self.set_result(style=DRAW)
        logger.debug('Draw')
        self.eog = True

    def set_result(self, style):
        for x in range(SIZE):
            for y in range(SIZE):
                self.field[x][y].setStyleSheet(style)

    def start(self):
        self.show()
        sys.exit(self.app.exec())
