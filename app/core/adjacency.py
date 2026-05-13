import numpy as np
from scipy.spatial import Delaunay
import networkx as nx

from app.data.loader import Precinct


def build_adjacency(precincts: list[Precinct]) -> nx.Graph:
    # TODO: build an undirected graph where every precinct is a node and
    # edges connect geographic neighbours.
    #
    # How:
    #   1. Extract (lon, lat) coords into a numpy array
    #   2. Run scipy.spatial.Delaunay on the coords
    #   3. For each triangle simplex (3 indices), add all 3 pairs as edges
    #   4. Return the networkx.Graph
    #
    # Result: a planar neighbour graph — any two precincts that share a
    # Voronoi edge will be connected here, which the solver uses to guarantee
    # contiguous districts.
    pass
