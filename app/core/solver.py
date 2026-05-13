import heapq

import numpy as np
import networkx as nx

from app.data.loader import Precinct


def _farthest_point_seeds(coords: np.ndarray, n: int) -> list[int]:
    # TODO: pick n indices that are maximally spread across the coordinate space.
    #
    # How (Farthest Point Sampling):
    #   1. Start from the point nearest to coords.mean() (geographic center)
    #   2. Keep a min_dists array = distance from each point to its nearest seed
    #   3. Each iteration: pick argmax(min_dists) as next seed, then update
    #      min_dists = min(min_dists, distance_to_new_seed)
    #   4. Set min_dists[new_seed] = 0 so it can't be picked again
    #
    # Returns list of n precinct indices. Guarantees seeds don't cluster.
    pass


def solve(precincts: list[Precinct], graph: nx.Graph, n_districts: int) -> dict[int, int]:
    # TODO: partition precincts into n_districts contiguous, population-balanced groups.
    #
    # How (greedy BFS with min-heap):
    #   1. Pick seeds with _farthest_point_seeds — one per district
    #   2. Assign each seed to its district, record district_population
    #   3. Push all unassigned neighbours into a min-heap keyed by district_population
    #   4. Pop the heap: assign the precinct to that district, add its population,
    #      push its unassigned neighbours back in
    #   5. A district only ever claims neighbours of its own nodes → always contiguous
    #   6. Fallback: assign any disconnected precinct to district 0
    #
    # Returns {precinct_id: district_id}
    pass
