import unittest
import json
from fractions import Fraction
from pathlib import Path

from dpp_core import (
    build_certificate,
    entropy_term_interval,
    exact_event_mass_polys,
    parse_fraction,
    poly_eval,
    poly_to_json,
    principal_minor_poly,
    tiny_example_payload,
)


class DppCoreTests(unittest.TestCase):
    def test_tiny_example_determinants(self):
        payload = tiny_example_payload()
        k_matrix = [[Fraction(x) for x in row] for row in payload["K"]]
        d_matrix = [[Fraction(x) for x in row] for row in payload["D"]]
        self.assertEqual(poly_to_json(principal_minor_poly(k_matrix, d_matrix, (0,))), ["1/5", "2/5"])
        self.assertEqual(poly_to_json(principal_minor_poly(k_matrix, d_matrix, (1,))), ["2/5", "-1/5"])
        self.assertEqual(
            poly_to_json(principal_minor_poly(k_matrix, d_matrix, (0, 1))),
            ["17/225", "26/225", "-73/900"],
        )

    def test_tiny_example_exact_event_masses(self):
        payload = tiny_example_payload()
        k_matrix = [[Fraction(x) for x in row] for row in payload["K"]]
        d_matrix = [[Fraction(x) for x in row] for row in payload["D"]]
        principal = {
            subset: principal_minor_poly(k_matrix, d_matrix, subset)
            for subset in [(), (0,), (1,), (0, 1)]
        }
        masses = exact_event_mass_polys(principal, 2)
        self.assertEqual(poly_to_json(masses[()]), ["107/225", "-19/225", "-73/900"])
        self.assertEqual(poly_to_json(masses[(0,)]), ["28/225", "64/225", "73/900"])
        self.assertEqual(poly_to_json(masses[(1,)]), ["73/225", "-71/225", "73/900"])
        self.assertEqual(poly_to_json(masses[(0, 1)]), ["17/225", "26/225", "-73/900"])

    def test_tiny_example_certifies_gap_and_curvature(self):
        cert = build_certificate(tiny_example_payload())
        self.assertEqual(cert["certificate_status"], "CERTIFIED")
        self.assertTrue(cert["feasibility"]["certified"])
        self.assertEqual(cert["events"]["family"], "all")
        self.assertEqual(cert["events"]["selected_mass_poly_t_power_basis"], ["1"])
        self.assertEqual(cert["entropy"]["chord_gap"]["sign"], "positive")
        self.assertEqual(cert["entropy"]["curvature"]["sign"], "negative")

    def test_default_entropy_family_is_all_exact_events(self):
        payload = tiny_example_payload()
        del payload["event_family"]
        cert = build_certificate(payload)
        self.assertEqual(cert["canonical_input"]["event_family"], "all")
        self.assertEqual(cert["events"]["selected_mass_poly_t_power_basis"], ["1"])

    def test_diagonal_bernoulli_exact_mass_not_inclusion_minor(self):
        payload = {
            "K": [["1/3", "0"], ["0", "1/4"]],
            "D": [["1/6", "0"], ["0", "1/12"]],
            "interval": ["0", "1"],
            "chord": {"t": "1/2"},
            "curvature": {"t": "1/2"},
            "bernstein_depth": 4,
            "log_bits": 100,
        }
        cert = build_certificate(payload)
        masses = {
            tuple(item["subset"]): item["q_poly_t_power_basis"]
            for item in cert["exact_event_mass_polynomials"]
        }
        self.assertEqual(masses[(0,)], ["1/4", "7/72", "-1/72"])
        self.assertNotEqual(masses[(0,)], ["1/3", "1/6"])
        self.assertEqual(cert["events"]["selected_mass_poly_t_power_basis"], ["1"])
        self.assertEqual(cert["certificate_status"], "CERTIFIED")

    def test_zero_entropy_term_is_limit_zero(self):
        self.assertEqual(entropy_term_interval(Fraction(0), 80), (Fraction(0), Fraction(0)))

    def test_refuses_non_probability_event_mass(self):
        payload = tiny_example_payload()
        payload["event_family"] = "listed"
        payload["events"] = [[0]]
        cert = build_certificate(payload)
        self.assertEqual(cert["certificate_status"], "REFUSED")
        self.assertIn("selected event family does not have exact total mass polynomial 1", cert["failure_reasons"])

    def test_refuses_negative_exact_event_mass_even_when_inclusion_minor_positive(self):
        payload = {
            "K": [["3/2", "0"], ["0", "1/4"]],
            "D": [["0", "0"], ["0", "0"]],
            "interval": ["0", "1"],
            "chord": {"t": "1/2"},
            "bernstein_depth": 2,
            "log_bits": 80,
        }
        cert = build_certificate(payload)
        self.assertEqual(cert["certificate_status"], "REFUSED")
        self.assertTrue(any(reason.startswith("exact event mass") for reason in cert["failure_reasons"]))

    def test_refuses_nonsymmetric_frozen_kernel_path(self):
        payload = tiny_example_payload()
        payload["K"][0][1] = "1/7"
        cert = build_certificate(payload)
        self.assertEqual(cert["certificate_status"], "REFUSED")
        self.assertIn(
            "K and D must be symmetric rational matrices for the frozen marginal-kernel certificate",
            cert["failure_reasons"],
        )

    def test_public_seed_chord_case_if_available(self):
        seed_path = Path(__file__).resolve().parents[1] / "artifacts" / "seed_chord_case.json"
        if not seed_path.exists():
            self.skipTest("research/T3/artifacts/seed_chord_case.json is not present in this checkout")
        raw = json.loads(seed_path.read_text(encoding="utf-8"))
        seed = raw.get("payload", raw)
        cert = build_certificate(raw)
        mass_polys = {
            tuple(item["subset"]): [parse_fraction(coeff) for coeff in item["q_poly_t_power_basis"]]
            for item in cert["exact_event_mass_polynomials"]
        }
        for point_name, expected in raw.get("diagnostic_masses", {}).items():
            t = parse_fraction(seed["chord"][point_name])
            for subset_text, expected_value in expected.items():
                subset = tuple(json.loads(subset_text))
                self.assertEqual(poly_eval(mass_polys[subset], t), parse_fraction(expected_value))
        self.assertEqual(cert["events"]["family"], "all")
        self.assertEqual(cert["events"]["selected_mass_poly_t_power_basis"], ["1"])
        self.assertEqual(cert["certificate_status"], "CERTIFIED")
        self.assertEqual(cert["entropy"]["chord_gap"]["sign"], "positive")
        self.assertIn(
            "Entropy uses selected exact outcome masses q(S), with all subsets selected by default.",
            cert["assumptions"],
        )


if __name__ == "__main__":
    unittest.main()
