import itertools
import json
import sys
from fractions import Fraction as Q
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "research" / "T1" / "tools"))

from bridge_check import check, graph_bridges  # noqa: E402


def qmat(rows):
    return [[str(Q(x)) for x in row] for row in rows]


def expect(name, raw, status=None, sign=None):
    result = check(raw)
    if status is not None and result.get("status") != status:
        raise AssertionError((name, result))
    if sign is not None and result.get("curvature_sign") != sign:
        raise AssertionError((name, result))
    return {"name": name, "result": result}


def brute_bridges(n, edges):
    expected = set()
    for edge in edges:
        start, goal = edge
        seen = {start}
        stack = [start]
        remaining = edges - {edge}
        while stack:
            v = stack.pop()
            for x, y in remaining:
                w = y if x == v else x if y == v else None
                if w is not None and w not in seen:
                    seen.add(w)
                    stack.append(w)
        if goal not in seen:
            expected.add(edge)
    return expected


def graph_matrix(n, edges):
    return [[int(tuple(sorted((i, j))) in edges) for j in range(n)] for i in range(n)]


def main():
    artifacts = REPO / "research" / "T1" / "artifacts"
    results = []
    for blocks, active_count in ((2, 1), (10, 9)):
        raw = json.loads((artifacts / f"triangles_{blocks}.json").read_text())
        item = expect(f"artifact triangles_{blocks}", raw, "APPLICABLE", "negative")
        if len(item["result"]["active_edges"]) != active_count:
            raise AssertionError((blocks, item["result"]["active_edges"]))
        if item["result"]["event_probabilities_evaluated"] != 0:
            raise AssertionError((blocks, item["result"]))
        results.append(item)

    disconnected_bridge = {
        "K": qmat(
            [
                [Q(1, 2), Q(1, 10), 0, 0],
                [Q(1, 10), Q(1, 2), 0, 0],
                [0, 0, Q(1, 2), 0],
                [0, 0, 0, Q(1, 2)],
            ]
        ),
        "A": qmat([[0, Q(1, 20), 0, 0], [-Q(1, 20), 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    }
    results.append(expect("disconnected graph with isolated vertices", disconnected_bridge, "APPLICABLE", "negative"))

    path_two_bridges = {
        "K": qmat(
            [
                [Q(1, 2), Q(1, 20), 0],
                [Q(1, 20), Q(1, 2), Q(1, 30)],
                [0, Q(1, 30), Q(1, 2)],
            ]
        ),
        "A": qmat([[0, Q(1, 40), 0], [-Q(1, 40), 0, Q(1, 50)], [0, -Q(1, 50), 0]]),
    }
    results.append(expect("path with two active bridges", path_two_bridges, "APPLICABLE", "negative"))

    zero_direction = json.loads((artifacts / "triangles_2.json").read_text())
    zero_direction["A"] = [[0 for _ in row] for row in zero_direction["A"]]
    results.append(expect("zero direction", zero_direction, "APPLICABLE", "zero"))

    cycle_edge = json.loads((artifacts / "triangles_2.json").read_text())
    cycle_edge["A"][0][1] = "1/30"
    cycle_edge["A"][1][0] = "-1/30"
    results.append(expect("active edge inside triangle cycle", cycle_edge, "INCONCLUSIVE"))

    absent_edge = json.loads((artifacts / "triangles_2.json").read_text())
    absent_edge["A"][0][5] = "1/30"
    absent_edge["A"][5][0] = "-1/30"
    results.append(expect("active absent edge", absent_edge, "INCONCLUSIVE"))

    nonsymmetric_k = {"K": [["1/2", "0"], ["1/10", "1/2"]], "A": [[0, 0], [0, 0]]}
    results.append(expect("nonsymmetric K", nonsymmetric_k, "INVALID_INPUT"))

    nonskew_a = {"K": [["1/2", "1/10"], ["1/10", "1/2"]], "A": [[0, "1/20"], ["1/20", 0]]}
    results.append(expect("nonskew A", nonskew_a, "INVALID_INPUT"))

    float_input = {"K": [[0.5]], "A": [[0]]}
    results.append(expect("float rejected", float_input, "INVALID_INPUT"))

    not_strict = {"K": [[0]], "A": [[0]]}
    results.append(expect("not strict contraction", not_strict, "OUTSIDE_DOMAIN"))

    graph_count = 0
    for n in range(1, 6):
        pairs = list(itertools.combinations(range(n), 2))
        for mask in range(2 ** len(pairs)):
            edges = {edge for bit, edge in enumerate(pairs) if (mask >> bit) & 1}
            if graph_bridges(graph_matrix(n, edges)) != brute_bridges(n, edges):
                raise AssertionError((n, mask, edges, graph_bridges(graph_matrix(n, edges)), brute_bridges(n, edges)))
            graph_count += 1

    output = {
        "status": "PASS",
        "cases": results,
        "exhaustive_graph_cases_n_le_5": graph_count,
        "role": "adversarial checker-domain tests only; not a proof of theorem",
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
