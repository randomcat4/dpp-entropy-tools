import json
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exact_dpp_reference as ref


CASES_PATH = Path(__file__).with_name("adversarial_cases.json")


def load_case(name):
    data = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for case in data["cases"]:
        if case["name"] == name:
            return case
    raise AssertionError(f"missing case {name}")


class ExactDppReferenceTests(unittest.TestCase):
    def test_near_zero_and_zero_probability_limits(self):
        near = load_case("near_zero_l_ensemble")
        k, d, mode = ref.parse_case(near)
        jets = ref.probability_jets(k, d, Fraction(0), mode)
        tiny = next(j for j in jets if j.subset == (0,))
        self.assertGreater(tiny.p, 0)
        self.assertLess(tiny.p, Fraction(1, 10**20))

        near_result = ref.analyze_case(near)
        self.assertEqual(near_result["status"], "CANDIDATE")
        self.assertEqual(near_result["entropy_points"][0]["entropy"]["zero_terms"], [])

        zero = ref.analyze_case(load_case("zero_probability_marginal_boundary"))
        self.assertEqual(zero["status"], "CANDIDATE")
        self.assertEqual(
            sorted(zero["entropy_points"][0]["entropy"]["zero_terms"]),
            ["{0,1}", "{0}"],
        )

    def test_repeated_eigen_diagonal_case_has_exact_jets(self):
        case = load_case("repeated_eigen_diagonal_l_ensemble")
        k, d, mode = ref.parse_case(case)
        jets = ref.probability_jets(k, d, Fraction(0), mode)
        self.assertEqual([j.p for j in jets], [Fraction(1, 4)] * 4)
        self.assertEqual(sum(j.p1 for j in jets), 0)
        self.assertEqual(sum(j.p2 for j in jets), 0)

        curvature = ref.curvature_interval(jets, 190)
        self.assertEqual(curvature["classification"], "CERTIFIED_NEGATIVE")
        self.assertLess(ref.parse_fraction(curvature["interval"]["hi_exact"]), 0)

    def test_tiny_gap_rejects_float_sized_false_candidate(self):
        result = ref.analyze_case(load_case("tiny_gap_float_misleading"))
        self.assertEqual(result["status"], "CANDIDATE")
        self.assertEqual(result["chord_gap"]["classification"], "CERTIFIED_POSITIVE")
        self.assertEqual(result["candidate_check"]["status"], "REJECTED")

        certified_lower = ref.parse_fraction(result["chord_gap"]["interval"]["lo_exact"])
        self.assertGreater(certified_lower, 0)
        self.assertLess(certified_lower, Fraction(1, 10**15))
        self.assertLess(abs(float(result["float_chord_gap"]["value"])), 1e-15)

    def test_invalid_inputs_are_rejected_without_tolerance(self):
        negative = ref.analyze_case(load_case("invalid_negative_l_weight"))
        self.assertEqual(negative["status"], "REJECTED_INPUT")
        self.assertEqual(negative["feasibility"]["status"], "REJECTED")

        nonsymmetric = ref.analyze_case(load_case("invalid_nonsymmetric_input"))
        self.assertEqual(nonsymmetric["status"], "REJECTED_INPUT")
        self.assertEqual(nonsymmetric["error_type"], "ReferenceInputError")

    def test_restart_friendly_outputs_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            partial = ref.run_cases(CASES_PATH, out, stop_after=3)
            self.assertFalse(partial["complete"])
            self.assertEqual(partial["completed_count"], 3)
            self.assertTrue((out / "near_zero_l_ensemble.json").exists())

            complete_one = ref.run_cases(CASES_PATH, out)
            complete_two = ref.run_cases(CASES_PATH, out)
            self.assertTrue(complete_one["complete"])
            self.assertEqual(complete_one["certificate_hash"], complete_two["certificate_hash"])


if __name__ == "__main__":
    unittest.main()
