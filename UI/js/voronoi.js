/**
 * Builds and renders a Voronoi diagram over the Leaflet map.
 *
 * Flow:
 *   1. Attach an SVG layer to Leaflet's overlayPane (Leaflet manages its CSS transform on pan)
 *   2. On viewreset / zoomend / moveend: project each precinct's lat/lon to layer-point
 *      pixel coords and rebuild the Voronoi diagram from scratch
 *   3. Each cell is a <path> coloured by the precinct's political lean
 *   4. Clicking a cell populates the sidebar info panel
 */
/**
 * borderRing: array of [lon, lat] pairs from the GeoJSON outer ring.
 * On every redraw the ring is projected to layer-point coords and used as
 * an SVG <clipPath> so Voronoi cells are masked to Israel's shape.
 */
export function initVoronoiLayer(map, precincts, borderRing) {
  // L.svg() creates an SVG element inside overlayPane and keeps its CSS transform
  // in sync with the map — so panning animates smoothly without a full redraw
  const svgLayer = L.svg();
  svgLayer.addTo(map);

  const svg = svgLayer._container;
  svg.style.pointerEvents = 'none'; // SVG container itself is transparent to mouse

  // Build the <defs> → <clipPath> → <path> structure once.
  // The clipPath's <path d> is updated on every redraw as coordinates change.
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  const clipPath = document.createElementNS('http://www.w3.org/2000/svg', 'clipPath');
  clipPath.setAttribute('id', 'israel-clip');
  const clipShape = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  clipPath.appendChild(clipShape);
  defs.appendChild(clipPath);
  svg.appendChild(defs);

  // All cells live inside this <g>. clip-path masks everything outside Israel.
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('clip-path', 'url(#israel-clip)');
  svg.appendChild(g);

  const draw = () => {
    // Re-project the border ring in the current coordinate frame and update clipPath
    clipShape.setAttribute('d', ringToLayerPath(map, borderRing));
    drawVoronoi(map, precincts, g);
  };

  // viewreset fires when the layer-point origin shifts (on zoom)
  // moveend fires after a pan completes and the transform is applied
  map.on('viewreset zoomend moveend', draw);
  draw();
}

/**
 * Projects a GeoJSON ring ([lon, lat] pairs) to layer-point pixel coords
 * and returns an SVG path string (M … L … Z).
 */
function ringToLayerPath(map, ring) {
  return ring.map(([lon, lat], i) => {
    const { x, y } = map.latLngToLayerPoint([lat, lon]);
    return `${i === 0 ? 'M' : 'L'}${x},${y}`;
  }).join(' ') + ' Z';
}

/**
 * Clears and redraws all Voronoi cells into <g>.
 * Must be called whenever the map's layer-point origin changes.
 */
function drawVoronoi(map, precincts, g) {
  // Project each precinct from geographic coords to layer-point pixel coords.
  // Layer-point coords are the coordinate system used by Leaflet's overlayPane SVG.
  const points = precincts.map(p => map.latLngToLayerPoint([p.lat, p.lon]));

  // Compute bounds in layer-point space from the visible container corners.
  // We add padding so cells near the edge are fully clipped rather than open.
  const pad = 200;
  const size = map.getSize();
  const tl = map.containerPointToLayerPoint([0, 0]);
  const br = map.containerPointToLayerPoint([size.x, size.y]);
  const bounds = [tl.x - pad, tl.y - pad, br.x + pad, br.y + pad];

  const delaunay = d3.Delaunay.from(points, p => p.x, p => p.y);
  const voronoi = delaunay.voronoi(bounds);

  g.innerHTML = '';

  precincts.forEach((precinct, i) => {
    const cellPath = voronoi.renderCell(i);
    if (!cellPath) return;

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', cellPath);
    path.setAttribute('fill', precinctColor(precinct));
    path.setAttribute('class', 'voronoi-cell');
    path.style.pointerEvents = 'all'; // individual cells receive clicks

    path.addEventListener('click', () => showPrecinctInfo(precinct));
    g.appendChild(path);
  });
}

/**
 * Maps a precinct's vote shares to a fill colour.
 *   Arab-majority precincts → green
 *   Left-leaning           → blue  (stronger = deeper blue)
 *   Right-leaning          → red   (stronger = deeper red)
 */
function precinctColor(precinct) {
  const total = (precinct.left || 0) + (precinct.right || 0) + (precinct.arab || 0);
  if (total === 0) return '#888';

  const arabShare = (precinct.arab || 0) / total;
  if (arabShare > 0.5) return `hsl(145, 55%, 42%)`;

  // lean: +1 = fully left (blue), -1 = fully right (red)
  const lean = ((precinct.left || 0) - (precinct.right || 0)) / total;

  if (lean >= 0) {
    // blue = not bibi, intensity proportional to lean
    const l = Math.round(65 - lean * 30);
    return `hsl(4, 75%, ${l}%)`;
  } else {
    // red = bibi, intensity proportional to lean magnitude
    const l = Math.round(65 + lean * 30); // lean is negative so this increases
    return `hsl(220, 75%, ${l}%)`;
  }
}

/**
 * Writes precinct details into the sidebar info panel.
 */
function showPrecinctInfo(precinct) {
  const panel = document.getElementById('precinct-info');
  if (!panel) return;

  const total = (precinct.left || 0) + (precinct.right || 0) + (precinct.arab || 0);
  const pct = v => total ? Math.round((v / total) * 100) : 0;

  panel.innerHTML = `
    <h3>${precinct['yisuv name'] || precinct.address || '—'}</h3>
    <p class="info-row"><span>אוכלוסייה</span><span>${precinct.population ?? '—'}</span></p>
    <p class="info-row"><span>קולות</span><span>${total}</span></p>
    <hr/>
    <p class="info-row left-color"><span>לא ביבי</span><span>${precinct.left ?? 0} (${pct(precinct.left)}%)</span></p>
    <p class="info-row right-color"><span>ביבי</span><span>${precinct.right ?? 0} (${pct(precinct.right)}%)</span></p>
    <p class="info-row arab-color"><span>ערבי</span><span>${precinct.arab ?? 0} (${pct(precinct.arab)}%)</span></p>
  `;
}
