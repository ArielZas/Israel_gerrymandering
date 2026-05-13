from app.data.loader import Precinct


def compute_district_results(
    assignment: dict[int, int], precincts: list[Precinct]
) -> dict[int, dict]:
    # TODO: aggregate votes per district and determine winner.
    #
    # How:
    #   1. Build id_to_precinct lookup
    #   2. For each (precinct_id, district_id) in assignment, sum left/right/arab
    #      votes into a per-district totals dict
    #   3. For each district, winner = max(votes, key=votes.get)
    #
    # Returns {district_id: {'winner': str, 'votes': {'left', 'right', 'arab'}}}
    pass


def seat_summary(district_results: dict[int, dict]) -> dict[str, int]:
    # TODO: count how many districts each bloc wins.
    #
    # How: iterate district_results.values(), tally d['winner'] into a counter
    #
    # Returns {'right': N, 'left': N, 'arab': N}
    pass
