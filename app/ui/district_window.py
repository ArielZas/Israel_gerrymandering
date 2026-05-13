from PyQt6.QtWidgets import QMainWindow, QDockWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

from app.ui.results_panel import ResultsPanel

# TODO: define _MAP_HTML — an HTML string containing:
#   - Leaflet CSS + JS loaded from unpkg CDN
#   - A full-page <div id="map">
#   - L.map centered on Israel [31.5, 35.0] zoom 7 with OSM tile layer
#   - JS function renderDistricts(geojson): calls L.geoJSON with style
#     (fillColor from feature.properties.color, fillOpacity 0.65, black border weight 2)
#     and a tooltip showing district number, winner, and vote counts
_MAP_HTML = ""


class DistrictWindow(QMainWindow):
    def __init__(self, district_geojson: str, district_results: dict, parent=None):
        # TODO:
        #   1. setWindowTitle, resize(1400, 900)
        #   2. Create QWebEngineView, setHtml(_MAP_HTML), setCentralWidget
        #   3. Connect loadFinished signal: when ok=True, call
        #      page().runJavaScript(f"renderDistricts({district_geojson});")
        #   4. Create ResultsPanel, call update_results(district_results)
        #   5. Wrap in QDockWidget, addDockWidget to RightDockWidgetArea
        pass
