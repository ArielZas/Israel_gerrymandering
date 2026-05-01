/**
 * Initialises the Leaflet map centred on Israel.
 * Returns the map instance.
 */
export function initMap(containerId) {
  const map = L.map(containerId).setView([31.5, 34.8], 8);

  // OpenStreetMap tiles — free, no API key required
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(map);

  return map;
}

/**
 * Converts a geographic [lat, lon] to a Leaflet pixel point on the current map.
 * Used by the Voronoi layer to project coordinates into screen space.
 * Note: pixel coords change on every zoom/pan — call this only inside drawVoronoi.
 */
export function latLonToPoint(map, lat, lon) {
  return map.latLngToLayerPoint([lat, lon]);
}
