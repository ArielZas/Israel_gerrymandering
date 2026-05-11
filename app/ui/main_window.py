from pathlib import Path
import json
import numpy as np
from scipy.spatial import KDTree
from shapely.ops import voronoi_diagram, unary_union
from shapely.geometry import MultiPoint, shape, mapping

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView

from app.data.loader import load_precincts

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_BORDER_PATH = _PROJECT_ROOT / 'boundaries' / 'Israel_jns_map.geojson'

_BLOC_COLORS = {
    'right': '#4477dd',
    'left':  '#e84040',
    'arab':  '#44aa55',
}

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

        function renderPrecincts(geojson) {
            if (precinctLayer) { map.removeLayer(precinctLayer); }
            precinctLayer = L.geoJSON(geojson, {
                style: function(f) {
                    return {
                        fillColor: f.properties.color,
                        weight: 0.5,
                        color: '#333',
                        fillOpacity: 0.65
                    };
                },
                onEachFeature: function(f, layer) {
                    var p = f.properties;
                    layer.bindTooltip(
                        '<b>' + p.name + '</b><br/>' +
                        'Right: ' + p.right + '&emsp;' +
                        'Left: '  + p.left  + '&emsp;' +
                        'Arab: '  + p.arab
                    );
                }
            }).addTo(map);
        }

        // TODO: renderDistricts(geojson) — overlay computed district boundaries
    </script>
</body>
</html>
"""


def _load_border():
    with open(_BORDER_PATH, encoding='utf-8') as f:
        gj = json.load(f)
    features = gj['features'] if gj['type'] == 'FeatureCollection' else [gj]
    return unary_union([shape(feat['geometry']) for feat in features])


def _build_voronoi_geojson(precincts, israel_border):
    valid = [p for p in precincts if p.lat and p.lon]
    coords = np.array([(p.lon, p.lat) for p in valid])

    regions = voronoi_diagram(MultiPoint(coords))
    tree = KDTree(coords)

    features = []
    for region in regions.geoms:
        clipped = region.intersection(israel_border)
        if clipped.is_empty:
            continue

        _, idx = tree.query([region.centroid.x, region.centroid.y])
        p = valid[idx]

        dominant = max({'left': p.left, 'right': p.right, 'arab': p.arab}, key=lambda k: {'left': p.left, 'right': p.right, 'arab': p.arab}[k])

        features.append({
            'type': 'Feature',
            'geometry': mapping(clipped),
            'properties': {
                'color': _BLOC_COLORS[dominant],
                'name': p.name,
                'left': p.left,
                'right': p.right,
                'arab': p.arab,
            },
        })

    return json.dumps({'type': 'FeatureCollection', 'features': features})


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Israel Gerrymandering")
        self.resize(1200, 800)

        # TODO: add ConfigPanel (left dock) and ResultsPanel (right dock)

        self._map_view = QWebEngineView()
        self._map_view.setHtml(_MAP_HTML)
        self._map_view.loadFinished.connect(self._on_map_loaded)
        self.setCentralWidget(self._map_view)

    def _on_map_loaded(self, ok):
        if not ok:
            return
        # TODO: run in a background QThread to avoid blocking the UI
        precincts = load_precincts()
        israel_border = _load_border()
        geojson = _build_voronoi_geojson(precincts, israel_border)
        self._map_view.page().runJavaScript(f"renderPrecincts({geojson});")
