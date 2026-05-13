from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt6.QtCore import pyqtSignal


class ConfigPanel(QWidget):
    run_requested = pyqtSignal(int)  # emits n_districts when Run is clicked

    def __init__(self):
        # TODO: build the layout:
        #   - QLabel "Number of Districts"
        #   - QSpinBox (range 2–120, default 10) → self._spinbox
        #   - QPushButton "Run Solver" → on click emit run_requested(spinbox.value())
        #   - addStretch() at the bottom
        pass
