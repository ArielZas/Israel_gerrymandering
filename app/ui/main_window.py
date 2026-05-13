from collections import defaultdict
from pathlib import Path
import json

import numpy as np
from scipy.spatial import KDTree
from shapely.ops import voronoi_diagram, unary_union
from shapely.geometry import MultiPoint, shape, mapping

from PyQt6.QtWidgets import QMainWindow, QDockWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

from app.data.loader import load_precincts, Precinct
from app.core.adjacency import build_adjacency
from app.core.solver import solve
from app.core.metrics import compute_district_results
from app.ui.config_panel import ConfigPanel
from app.ui.district_window import DistrictWindow

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_BORDER_PATH  = _PROJECT_ROOT / 'boundaries' / 'Israel_jns_map.geojson'
_BLOC_COLORS  = {'right': '#e84040', 'left': '#4477dd', 'arab': '#44aa55'}

_MAP_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>html, body, #map { height: 100%; margin: 0; padding: 0; }</style>
    <link rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([31.5, 35.0], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);

        var precinctLayer = null;

        // TODO: implement renderPrecincts(geojson) — L.geoJSON with fillColor
        // from feature.properties.color, thin border, fillOpacity 0.65,
        // tooltip showing precinct name and left/right/arab vote counts
    </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _load_border():
    # TODO: open _BORDER_PATH as JSON, extract all features, convert each
    # geometry to a shapely shape(), return unary_union of all of them
    pass


def _compute_voronoi_polygons(precincts: list[Precinct], border) -> dict[int, object]:
    # TODO: compute a Voronoi diagram for all precinct lat/lon points, then
    # clip each region to the Israel border and map it back to its precinct.
    #
    # How:
    #   1. Build numpy coords array [(lon, lat), ...]
    #   2. Call shapely.ops.voronoi_diagram(MultiPoint(coords))
    #   3. For each region: clip with region.intersection(border)
    #   4. Find owning precinct: KDTree query on region.centroid → nearest coord index
    #   5. Store {precinct.id: clipped_polygon}
    #
    # Returns dict[precinct_id → shapely Polygon]
    pass


def _precincts_to_geojson(precincts: list[Precinct], polygons: dict) -> str:
    # TODO: convert the precinct polygons to a GeoJSON FeatureCollection string.
    #
    # For each polygon: determine dominant bloc (max of left/right/arab),
    # pick color from _BLOC_COLORS, build a GeoJSON Feature with geometry
    # from mapping(poly) and properties {color, name, right, left, arab}.
    # Return json.dumps of the FeatureCollection.
    pass


def _districts_to_geojson(
    assignment: dict[int, int], polygons: dict, results: dict
) -> str:
    # TODO: merge precinct polygons per district and serialise to GeoJSON.
    #
    # How:
    #   1. Group polygons by district_id using assignment
    #   2. For each district: unary_union its polygons → one district polygon
    #   3. Look up winner + votes from results dict
    #   4. Build GeoJSON Feature with color from _BLOC_COLORS[winner]
    #
    # Returns json.dumps of the FeatureCollection.
    pass


# ---------------------------------------------------------------------------
# Main window (precinct view)
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Israel Gerrymandering — Precincts")
        self.resize(1200, 800)

        self._precincts = None
        self._polygons  = None
        self._district_window = None

        self._map_view = QWebEngineView()
        self._map_view.setHtml(_MAP_HTML)
        self._map_view.loadFinished.connect(self._on_map_loaded)
        self.setCentralWidget(self._map_view)

        # TODO: add ConfigPanel in a left QDockWidget once config_panel.py is implemented

    def _on_map_loaded(self, ok: bool) -> None:
        # TODO: called once the Leaflet map is ready in the WebEngine.
        #   1. load_precincts() → self._precincts
        #   2. _load_border() → border
        #   3. _compute_voronoi_polygons(precincts, border) → self._polygons
        #   4. _precincts_to_geojson(precincts, polygons) → geojson string
        #   5. page().runJavaScript("renderPrecincts(<geojson>);")
        pass

    def _on_run_solver(self, n_districts: int) -> None:
        # TODO: triggered by ConfigPanel when user clicks Run Solver.
        #   1. Guard: return if precincts or polygons not loaded yet
        #   2. build_adjacency(precincts) → graph
        #   3. solve(precincts, graph, n_districts) → assignment
        #   4. compute_district_results(assignment, precincts) → results
        #   5. _districts_to_geojson(assignment, polygons, results) → geojson
        #   6. Open DistrictWindow(geojson, results) → store in self._district_window
        #      (must keep reference or Python garbage-collects the window)
        #   7. self._district_window.show()
        pass
