"""Check the candidate wire contract and examples, never numerical evidence."""

import copy
import hashlib
import json
import re
import sys
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parent
MAX_BYTES = 1024 * 1024
RATIONAL = re.compile(r"^(0|-?[1-9][0-9]*)/[1-9][0-9]*$")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, "duplicate JSON key: " + key)
        obj[key] = value
    return obj


def reject_constant(value):
    raise ValueError("non-finite JSON constant: " + value)


def parse(raw):
    require(len(raw) <= MAX_BYTES, "input byte budget exceeded")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def exact_values(value):
    require(not isinstance(value, float), "floating-point JSON values forbidden")
    if isinstance(value, dict):
        for child in value.values():
            exact_values(child)
    elif isinstance(value, list):
        for child in value:
            exact_values(child)
    elif isinstance(value, str) and RATIONAL.fullmatch(value):
        number = Fraction(value)
        require(value == f"{number.numerator}/{number.denominator}",
                "noncanonical rational: " + value)


def interval(values, nondegenerate=False):
    lower, upper = map(Fraction, values)
    require(lower < upper if nondegenerate else lower <= upper,
            "unordered or degenerate interval")
    return lower, upper


def validate_request(request, validator):
    validator.validate(request)
    exact_values(request)
    n = len(request["K"])
    for field in ("K", "D"):
        matrix = request[field]
        require(len(matrix) == n and all(len(row) == n for row in matrix),
                "matrix shape mismatch")
        require(all(matrix[i][j] == matrix[j][i]
                    for i in range(n) for j in range(n)), "matrix not symmetric")
    a, b = interval(request["path"], nondegenerate=True)
    precision = request["precision"]
    require(precision["initial_bits"] <= precision["max_bits"], "precision order")
    require(Fraction(precision["absolute_width"]) > 0, "nonpositive target width")
    claim = request["claim"]
    if claim["type"] == "entropy_chord_gap":
        require(0 < Fraction(claim["weight"]) < 1, "invalid chord weight")
    elif claim["type"] == "curvature" and claim["scope"] == "point":
        require(a < Fraction(claim["at"]) < b, "curvature point not interior")


def validate_response(response, validator, request):
    validator.validate(response)
    exact_values(response)
    require(response["request_id"] == request["request_id"], "request ID mismatch")
    require(response["claim"] == request["claim"], "claim mismatch")
    c = response["coverage"]
    require(c["planned"] == 1, "single-request envelope required")
    require(0 <= c["certified"] <= c["completed"] <= c["started"] <= c["planned"],
            "invalid request coverage ordering")
    require(c["completed"] + c["failed"] <= c["started"], "failure counted complete")
    require(c["events_planned"] == 2 ** len(request["K"]), "wrong full-event denominator")
    require(0 <= c["events_completed"] <= c["events_represented"] <= c["events_planned"],
            "invalid explicit/logical event counts")
    require(c["cells_completed"] + c["cells_unresolved"] == c["cells_planned"],
            "leaf coverage does not add up")
    result = response["result"]
    if result is not None:
        claim_type = request["claim"]["type"]
        expected_units = {"feasibility": "none", "curvature": "nats_per_t_squared",
                          "entropy_chord_gap": "nats"}[claim_type]
        require(result["units"] == expected_units, "wrong result units")
        if result["bounds"] is not None:
            interval(result["bounds"])
        if claim_type == "feasibility":
            require(result["bounds"] is None, "feasibility is not a scalar bound")
    for artifact in response["evidence"]["artifacts"]:
        parts = artifact["path"].split("/")
        require(not PurePosixPath(artifact["path"]).is_absolute()
                and all(part not in (".", "..") for part in parts), "unsafe artifact path")
    if response["artifact_kind"] == "run":
        codes = {"proved": 0, "disproved": 1, "refused": 2, "incomplete": 3,
                 "failed": 4, "interrupted": 130}
        require(response["provenance"]["exit_code"] == codes[response["outcome"]],
                "exit code/outcome mismatch")
        require(c["planned_manifest_hash"] is not None, "missing planned manifest hash")
    if response["outcome"] in ("proved", "disproved"):
        evidence = response["evidence"]
        certificates = [a for a in evidence["artifacts"] if a["role"] == "certificate"]
        require(len(certificates) == 1, "one certificate file required")
        require(certificates[0]["sha256"] == response["provenance"]["certificate_hash"],
                "certificate hash fields differ")
        if request["claim"]["type"] == "feasibility":
            require(result["feasible"] is (response["outcome"] == "proved"),
                    "feasibility result disagrees with outcome")
        else:
            require(result["feasible"] is True and result["bounds"] is not None,
                    "entropy resolution needs feasibility and bounds")
            require(c["events_represented"] == c["events_planned"],
                    "entropy certificate lacks full event coverage")
            if request["include_events"]:
                require(c["events_completed"] == c["events_planned"],
                        "requested event export incomplete")
            require(c["cells_completed"] >= 1, "entropy certificate lacks a resolved domain")
            lower, upper = interval(result["bounds"])
            require(upper - lower <= Fraction(request["precision"]["absolute_width"]),
                    "requested width not met")
            signs = {"gt_zero": lower > 0, "ge_zero": lower >= 0,
                     "lt_zero": upper < 0, "le_zero": upper <= 0}
            opposite = {"gt_zero": upper <= 0, "ge_zero": upper < 0,
                        "lt_zero": lower >= 0, "le_zero": lower > 0}
            predicate = request["claim"]["predicate"]
            if response["outcome"] == "proved":
                require(signs[predicate], "bounds do not establish predicate")
            elif request["claim"]["scope"] == "point":
                require(opposite[predicate], "bounds do not disprove point predicate")
            # Path disproof requires a counterexample witness in the future checker.


def reject_case(label, operation):
    try:
        operation()
    except (ValueError, ValidationError):
        return label
    raise RuntimeError("invalid object accepted: " + label)


def changed(original, path, value):
    result = copy.deepcopy(original)
    target = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return result


def main():
    schema = parse((ROOT / "certificate.schema.json").read_bytes())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    request_bytes = (ROOT / "examples/scalar-curvature.request.json").read_bytes()
    response_bytes = (ROOT / "examples/scalar-curvature.response.json").read_bytes()
    request, response = parse(request_bytes), parse(response_bytes)
    validate_request(request, validator)
    validate_response(response, validator, request)
    # This exact scalar identity check does not create an engine certificate.
    k, d, t = Fraction(request["K"][0][0]), Fraction(request["D"][0][0]), Fraction(request["claim"]["at"])
    p = k + t * d
    curvature = -d * d * (1 / p + 1 / (1 - p))
    require(curvature == -1, "scalar arithmetic mismatch")
    require(all(0 <= k + Fraction(t) * d <= 1 for t in request["path"]),
            "scalar endpoints infeasible")
    require(interval(response["result"]["bounds"]) == (curvature, curvature),
            "illustrative bounds differ from scalar identity")
    rejected = []
    bad_requests = [
        ("float rational", ["K", 0, 0], 0.25),
        ("unreduced rational", ["K", 0, 0], "2/8"),
        ("noncanonical zero", ["D", 0, 0], "0/2"),
        ("zero denominator", ["D", 0, 0], "1/0"),
        ("ragged matrix", ["D"], [["1/2", "0/1"]]),
        ("reversed path", ["path"], ["1/1", "0/1"]),
        ("boundary curvature", ["claim", "at"], "0/1"),
        ("decreasing precision cap", ["precision", "max_bits"], 32),
        ("zero width", ["precision", "absolute_width"], "0/1"),
        ("float budget", ["limits", "threads"], 1.0),
        ("epsilon fallback", ["refusal", "zero_probability"], "epsilon"),
        ("unknown field", ["unexpected"], True),
        ("ambiguous chord", ["claim"], {"type": "entropy_chord_gap", "scope": "path", "predicate": "ge_zero"}),
        ("invalid chord weight", ["claim"], {"type": "entropy_chord_gap", "scope": "point", "weight": "2/1", "predicate": "ge_zero"}),
    ]
    for label, path, value in bad_requests:
        rejected.append(reject_case(label, lambda path=path, value=value:
                                   validate_request(changed(request, path, value), validator)))
    bad_responses = [
        ("illustration certification", ["coverage", "certified"], 1),
        ("self verification", ["state"], "VERIFIED"),
        ("wrong event denominator", ["coverage", "events_planned"], 1),
        ("missing leaf coverage", ["coverage", "cells_unresolved"], 0),
        ("fabricated illustration exit", ["provenance", "exit_code"], 0),
        ("unexecuted proof", ["outcome"], "proved"),
        ("mismatched claim", ["claim", "at"], "1/3"),
        ("wrong units", ["result", "units"], "nats"),
        ("reversed bounds", ["result", "bounds"], ["1/1", "-1/1"]),
    ]
    for label, path, value in bad_responses:
        rejected.append(reject_case(label, lambda path=path, value=value:
                                   validate_response(changed(response, path, value), validator, request)))
    rejected.append(reject_case("duplicate keys", lambda: parse(b'{"kind":"request","kind":"response"}')))
    rejected.append(reject_case("nonfinite constant", lambda: parse(b'{"x":NaN}')))
    print(json.dumps({
        "check": "contract_smoke_only", "status": "passed",
        "schema_validated": True, "examples_validated": 2,
        "negative_cases_rejected": len(rejected), "scalar_identity_checked": True,
        "strict_engine_requests_started": 0, "certified": 0,
        "python": sys.version.split()[0], "jsonschema": version("jsonschema"),
        "command": ["python", "research/T3/specs/check_contract.py"], "exit_code": 0,
        "example_input_sha256": hashlib.sha256(request_bytes).hexdigest(),
        "example_response_sha256": hashlib.sha256(response_bytes).hexdigest(),
        "certificate_hash": None
    }, indent=2))


if __name__ == "__main__":
    main()
