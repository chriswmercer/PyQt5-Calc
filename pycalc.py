import sys
from functools import partial

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

ERR_MSG = "Error"


class PyCalcUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calculator')
        self.setFixedSize(235, 235)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._create_display()
        self._create_buttons()

    def _create_display(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _create_buttons(self):
        self.buttons = {}
        buttons_layout = QGridLayout()
        buttons = { "7": (0, 0),
                    "8": (0, 1),
                    "9": (0, 2),
                    "/": (0, 3),
                    "C": (0, 4),
                    "4": (1, 0),
                    "5": (1, 1),
                    "6": (1, 2),
                    "*": (1, 3),
                    "(": (1, 4),
                    "1": (2, 0),
                    "2": (2, 1),
                    "3": (2, 2),
                    "-": (2, 3),
                    ")": (2, 4),
                    "0": (3, 0),
                    "00": (3, 1),
                    ".": (3, 2),
                    "+": (3, 3),
                    "=": (3, 4)}
        for buttonText, position in buttons.items():
            self.buttons[buttonText] = QPushButton(buttonText)
            self.buttons[buttonText].setFixedSize(40, 40)
            buttons_layout.addWidget(self.buttons[buttonText], position[0], position[1])

        self.generalLayout.addLayout(buttons_layout)

    def set_display_text(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def display_text(self):
        return self.display.text()

    def clear_display(self):
        self.set_display_text("")


class PyCalcController:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connect_signals()

    def _calculate_result(self):
        result = self._evaluate(expression=self._view.display_text())
        self._view.set_display_text(result)

    def _connect_signals(self):
        for button_text, button in self._view.buttons.items():
            if button_text not in ("=", "C"):
                button.clicked.connect(partial(self._build_expression, button_text))
            elif button_text == "C":
                button.clicked.connect(self._view.clear_display)
            elif button_text == "=":
                button.clicked.connect(self._calculate_result)
        self._view.display.returnPressed.connect(partial(self._calculate_result))

    def _build_expression(self, new_expression):
        if self._view.display_text() == ERR_MSG:
            self._view.clear_display()

        expression = self._view.display_text() + new_expression
        self._view.set_display_text(expression)


def evaluate_expression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERR_MSG
    return result


def main():
    pycalc = QApplication(sys.argv)

    view = PyCalcUI()
    model = evaluate_expression
    PyCalcController(model=model, view=view)
    view.show()

    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()