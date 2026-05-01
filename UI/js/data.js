/**
 * Fetches a GeoJSON file and returns the outer ring of the first feature's polygon
 * as an array of [lon, lat] pairs, ready to project onto the map.
 */
export async function loadBorder(geojsonPath) {
  const resp = await fetch(geojsonPath);
  const geo = await resp.json();
  // coordinates[0] is the outer ring; inner rings (holes) are ignored
  return geo.features[0].geometry.coordinates[0];
}

/**
 * Fetches and parses the precincts CSV at csvPath.
 * Uses PapaParse to download the file, convert column names to object keys
 * (header: true), and auto-cast numeric strings to numbers (dynamicTyping: true).
 * Rows missing lat or lon are dropped.
 * Returns a promise that resolves to an array of precinct objects.
 */
export async function loadPrecincts(csvPath) {
  return new Promise((resolve, reject) => {
    Papa.parse(csvPath, {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: ({ data }) => {
        const precincts = data.filter(p => p.lat && p.lon);
        resolve(precincts);
      },
      error: reject,
    });
  });
}
