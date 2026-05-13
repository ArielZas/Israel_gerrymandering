from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QColor

from app.core.metrics import seat_summary

_LABELS = {'right': 'Right', 'left': 'Left', 'arab': 'Arab'}
_BG     = {'right': '#ffcccc', 'left': '#ccdcff', 'arab': '#ccffcc'}


class ResultsPanel(QWidget):
    def __init__(self):
        # TODO: build the layout:
        #   - QLabel "<b>Seat Summary</b>"
        #   - QTableWidget(3 rows, 2 cols) with headers ["Bloc", "Seats"] → self._summary
        #   - QLabel "<b>Districts</b>"
        #   - QTableWidget(0 rows, 5 cols) with headers ["#","Winner","Right","Left","Arab"] → self._districts
        pass

    def update_results(self, district_results: dict) -> None:
        # TODO: populate both tables from district_results.
        #
        # Summary table:
        #   call seat_summary(district_results) → {bloc: count}
        #   fill self._summary row by row with bloc label and seat count
        #
        # Districts table:
        #   setRowCount to len(district_results)
        #   for each district (sorted by id): fill columns with district number,
        #   winner label, right/left/arab vote counts
        #   set each cell's background to _BG[winner]
        #   call resizeColumnsToContents() at the end
        pass
