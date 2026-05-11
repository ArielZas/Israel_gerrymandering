# Israel_gerrymandering
A project to create and gerrymander political districts in Israel

order:

The natural order, bottom-up:

1. data/loader.py first — everything else depends on having Precinct objects. Implement the dataclass and the CSV read. You can test it standalone with a print().

2. core/adjacency.py — build the neighbour graph from lat/lon. Delaunay triangulation (via scipy.spatial.Delaunay) is the easiest correct approach for this. Needed by the solver to enforce contiguity.

3. core/solver.py — this is the key decision point. Before writing code, pick the algorithm:

Graph partitioning (e.g. recursive bisection) — fast, deterministic, easy to implement first
Simulated annealing — flexible, finds better gerrymanders, but needs more tuning
I'd suggest starting with a simple greedy/recursive bisection just to get end-to-end working, then swapping in something smarter.

4. core/metrics.py — straightforward once you have assignments. Just aggregations over precinct votes.

5. UI last — wire config_panel → solver → results_panel, then add precinct dots and district boundary overlays to the map in main_window.py.

The one thing to decide before writing solver.py: do you want districts of equal population (like real electoral districts) or equal number of precincts? That constraint shapes the whole algorithm.



app/
├── main.py                  ✅ implemented
├── ui/
│   ├── __init__.py
│   ├── main_window.py       ✅ implemented (Leaflet map via QWebEngineView)
│   ├── config_panel.py      stub
│   └── results_panel.py     stub
├── core/
│   ├── __init__.py
│   ├── solver.py            stub
│   ├── metrics.py           stub
│   └── adjacency.py         stub
└── data/
    ├── __init__.py
    └── loader.py            stub (includes the Precinct dataclass sketch)
requirements.txt


Entry point

app/main.py — Boots the PyQt6 QApplication, creates the MainWindow, and starts the event loop. This is the only file you run.
UI layer (app/ui/) — everything the user sees

main_window.py — The top-level window (QMainWindow). Owns the Leaflet map in a QWebEngineView. Will also host the config and results panels as docks once those are built.
config_panel.py — The control sidebar: district count, algorithm choice, any tuning parameters. User sets inputs here and triggers a solver run.
results_panel.py — Displays the outcome after the solver runs: a table of districts with their vote breakdowns, and a seat-count summary (how many districts each bloc wins).
Core logic (app/core/) — no UI, pure computation

solver.py — Takes the list of precincts + a district count and returns an assignment: which precinct belongs to which district. The algorithm (graph partitioning, simulated annealing, etc.) lives here.
metrics.py — Given a district assignment, computes electoral statistics: seats won per bloc, wasted votes, efficiency gap.
adjacency.py — Builds a graph where each node is a precinct and edges connect geographic neighbours (using Delaunay or k-NN on lat/lon). The solver needs this to ensure districts are spatially contiguous.
Data access (app/data/)

loader.py — Reads data/precincts_merged.csv and returns structured Precinct objects (id, lat, lon, left/right/arab votes, population). Everything else in the app works with those objects, not raw CSV rows.
The flow in one line: loader feeds precincts → adjacency builds the graph → solver assigns districts → metrics scores the result → results_panel shows it, main_window draws it on the map.

