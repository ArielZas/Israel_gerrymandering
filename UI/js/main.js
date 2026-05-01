import { loadPrecincts, loadBorder } from './data.js';
import { initMap } from './map.js';
import { initVoronoiLayer } from './voronoi.js';

const CSV_PATH    = '../data/precincts_merged.csv';
const BORDER_PATH = '../boundaries/geoBoundaries-ISR-ADM0_simplified.geojson';

async function main() {
  // Load data in parallel — neither depends on the other
  const [precincts, borderRing] = await Promise.all([
    loadPrecincts(CSV_PATH),
    loadBorder(BORDER_PATH),
  ]);

  const map = initMap('map');
  initVoronoiLayer(map, precincts, borderRing);
}

main();
