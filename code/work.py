import pandas as pd
import requests
import time
from urllib.parse import quote
import geopandas as gpd
from shapely.geometry import Point

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------
df_addr = pd.read_excel("addresses.xlsx", dtype=str).fillna("")
df_res  = pd.read_csv("results.csv", dtype=str).fillna("")

# ------------------------------------------------------------
# 2. BUILD JOIN KEY (unique ID)
# ------------------------------------------------------------
df_addr["join_key"] = df_addr["סמל יישוב"].astype(str) + "_" + df_addr["סמל קלפי"].astype(str)
df_res["join_key"]  = df_res["סמל יישוב"].astype(str) + "_" + df_res["סמל קלפי"].astype(str)

# ------------------------------------------------------------
# 3. BUILD FULL ADDRESS STRING
#    (Adjust these column names according to your file!)
# ------------------------------------------------------------
def make_address(row):
    parts = []
    if "כתובת" in row and row["כתובת"]:
        parts.append(row["כתובת"])
    if "עיר" in row and row["עיר"]:
        parts.append(row["עיר"])
    return ", ".join(parts)

df_addr["full_address"] = df_addr.apply(make_address, axis=1)

# ------------------------------------------------------------
# 4. GOVMAP GEOCODER
# ------------------------------------------------------------
def geocode_govmap(address, city=""):
    url = (
        "https://govmap.gov.il/geocode.json?"
        f"address={quote(address)}&city={quote(city)}&format=1"
    )
    try:
        r = requests.get(url, timeout=5)
        j = r.json()
        if "result" in j and len(j["result"]) > 0:
            lat = j["result"][0]["Y"]
            lon = j["result"][0]["X"]
            return lat, lon
        return None, None
    except:
        return None, None

latitudes = []
longitudes = []

for i, row in df_addr.iterrows():
    addr = row["full_address"]
    city = row.get("עיר", "")
    lat, lon = geocode_govmap(addr, city)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(0.15)  # prevent rate limiting

df_addr["lat"] = latitudes
df_addr["lon"] = longitudes

# ------------------------------------------------------------
# 5. MERGE RESULTS + ADDRESSES
# ------------------------------------------------------------
df = df_res.merge(df_addr, on="join_key", how="left", suffixes=("_res", "_addr"))

# ------------------------------------------------------------
# 6. AGGREGATE PARTIES INTO BLOCS
#    (CHANGE PARTY COLUMN NAMES BELOW!)
# ------------------------------------------------------------

# ---- RIGHT BLOCK ----
right_parties = [
    "ליכוד", "ש\"ס", "יהדות התורה", 
    "הציונות הדתית", "עוצמה יהודית"
]

# ---- LEFT BLOCK ----
left_parties = [
    "יש עתיד", "העבודה", "מרצ",
    "המחנה הממלכתי", "כחול לבן", "ישראל ביתנו"
]

# ---- ARAB BLOCK ----
arab_parties = [
    "חד\"ש-תע\"ל", "רע\"מ", "בל\"ד"
]

# convert vote columns to integers safely
for col in right_parties + left_parties + arab_parties:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    else:
        print(f"WARNING: party column missing → {col}")

df["right_block"] = df[right_parties].sum(axis=1)
df["left_block"]  = df[left_parties].sum(axis=1)
df["arab_block"]  = df[arab_parties].sum(axis=1)

# ------------------------------------------------------------
# 7. KEEP ONLY THE IMPORTANT FIELDS
# ------------------------------------------------------------
df_final = df[[
    "join_key",
    "lat", "lon",
    "סמל יישוב", "סמל קלפי",
    "בעלי זכות בחירה",  # adjust if different name
    "right_block", "left_block", "arab_block"
]]

# ------------------------------------------------------------
# 8. EXPORT FINAL DATASET
# ------------------------------------------------------------
df_final.to_csv("kalpi_final_dataset.csv", index=False, encoding="utf-8-sig")

# Export GeoJSON for QGIS/Voronoi
geometry = [
    Point(float(lon), float(lat)) if pd.notnull(lat) and pd.notnull(lon) else None
    for lat, lon in zip(df_final["lat"], df_final["lon"])
]

gdf = gpd.GeoDataFrame(df_final, geometry=geometry, crs="EPSG:4326")
gdf.to_file("kalpi_final_dataset.geojson", driver="GeoJSON")

print("DONE — final dataset with coordinates + blocs successfully created!")
