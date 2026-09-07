import sys
import unittest
from decimal import Decimal
from decimal import localcontext
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import reference_implementation as ri


class GroupedReductionTests(unittest.TestCase):
    def assert_decimal_close(self, left, right, exponent="-80"):
        self.assertLess(abs(left - right), Decimal(f"1e{exponent}"))

    def assert_mobius_reduced_match(self, a, c, sizes, rows):
        cert = ri.positive_contraction_certificate_grouped(a, c, sizes, rows)
        self.assertEqual(cert["status"], "STRICT_POSITIVE_CONTRACTION")

        result = ri.compare_mobius_to_reduced(a, c, sizes, rows)
        self.assertEqual(result["mismatch_count"], 0)
        self.assertEqual(result["mobius_sum"], "1")
        self.assertEqual(result["reduced_sum"], "1")

        k = ri.build_grouped_k(a, c, sizes, rows)
        self.assertEqual(ri.event_probabilities_mobius(k), ri.event_probabilities_l_ensemble(k))

        reduced = ri.reduced_l_from_grouped(a, c, sizes, rows)
        h_reduced = ri.entropy_from_count_masses(ri.reduced_count_masses(reduced), precision=90)
        h_direct = ri.entropy_from_event_probabilities(ri.event_probabilities_mobius(k), precision=90)
        self.assert_decimal_close(h_reduced, h_direct)

    def test_random_like_n6_mobius_vs_reduced(self):
        self.assert_mobius_reduced_match(
            F(1, 3),
            ((F(1, 30), F(1, 70)), (F(1, 70), F(-1, 40))),
            (2, 3, 1),
            ((1, 0), (0, 1), (1, 1)),
        )

    def test_near_boundary_n8_mobius_vs_reduced(self):
        self.assert_mobius_reduced_match(
            F(1, 20),
            ((F(1, 200), F(1, 500)), (F(1, 500), F(-1, 300))),
            (2, 2, 2, 2),
            ((1, 0), (0, 1), (1, 1), (1, -1)),
        )

    def test_block_exchange_n8_standard_basis(self):
        self.assert_mobius_reduced_match(
            F(1, 2),
            (
                (F(1, 50), F(1, 200), F(-1, 300)),
                (F(1, 200), F(-1, 60), F(1, 250)),
                (F(-1, 300), F(1, 250), F(1, 70)),
            ),
            (2, 3, 3),
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        )

    def test_compatible_chord_gap_matches_direct_entropy(self):
        sizes = (2, 3, 1)
        rows = ((1, 0), (0, 1), (1, 1))
        a0 = F(1, 3)
        c0 = ((F(1, 30), F(1, 70)), (F(1, 70), F(-1, 40)))
        a1 = F(7, 20)
        c1 = ((F(1, 35), F(-1, 90)), (F(-1, 90), F(-1, 50)))
        theta = F(1, 2)

        gap_reduced = ri.chord_gap_reduced(a0, c0, a1, c1, sizes, rows, theta, precision=90)

        kt = ri.build_grouped_k(
            (a0 + a1) / 2,
            ri.scalar_mul(F(1, 2), ri.mat_add(ri.as_matrix(c0), ri.as_matrix(c1))),
            sizes,
            rows,
        )
        k0 = ri.build_grouped_k(a0, c0, sizes, rows)
        k1 = ri.build_grouped_k(a1, c1, sizes, rows)
        h0 = ri.entropy_from_event_probabilities(ri.event_probabilities_mobius(k0), precision=90)
        h1 = ri.entropy_from_event_probabilities(ri.event_probabilities_mobius(k1), precision=90)
        ht = ri.entropy_from_event_probabilities(ri.event_probabilities_mobius(kt), precision=90)
        with localcontext() as ctx:
            ctx.prec = 90
            gap_direct = +(ht - (h0 + h1) / Decimal(2))

        self.assert_decimal_close(gap_reduced, gap_direct)

    def test_gap_interval_sign_convention(self):
        gap = ri.chord_gap_interval(
            ri.DecimalInterval(Decimal("1.0"), Decimal("1.1")),
            ri.DecimalInterval(Decimal("1.2"), Decimal("1.3")),
            ri.DecimalInterval(Decimal("1.05"), Decimal("1.06")),
            theta=F(1, 2),
            precision=30,
        )
        self.assertEqual(gap.lo, Decimal("-0.15"))
        self.assertEqual(gap.hi, Decimal("-0.04"))

    def test_reduced_only_n12_probability_sum(self):
        sizes = (3, 3, 3, 3)
        rows = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
        c = (
            (F(1, 60), F(1, 300), 0, 0),
            (F(1, 300), F(-1, 80), F(1, 400), 0),
            (0, F(1, 400), F(1, 100), F(-1, 500)),
            (0, 0, F(-1, 500), F(-1, 120)),
        )
        cert = ri.positive_contraction_certificate_grouped(F(2, 5), c, sizes, rows)
        self.assertEqual(cert["status"], "STRICT_POSITIVE_CONTRACTION")
        masses = ri.reduced_count_masses(
            ri.reduced_l_from_grouped(F(2, 5), c, sizes, rows)
        )
        self.assertEqual(len(masses), 256)
        self.assertEqual(ri.probability_sum_from_count_masses(masses), F(1))

    def assert_block_exchange_exact_match(self, a_values, c, sizes):
        c_matrix = ri.as_matrix(c)
        c_ok, _ = ri.positive_definite_sylvester(c_matrix)
        ic_ok, _ = ri.positive_definite_sylvester(ri.mat_sub(ri.eye(len(c_matrix)), c_matrix))
        self.assertTrue(c_ok and ic_ok)
        result = ri.compare_mobius_to_block_exchange_reduced(a_values, c, sizes)
        self.assertEqual(result["mismatch_count"], 0)
        self.assertEqual(result["mobius_sum"], "1")
        self.assertEqual(result["l_ensemble_sum"], "1")
        self.assertEqual(result["reduced_sum"], "1")
        self.assertEqual(result["orbit_size_sum"], 2 ** sum(sizes))
        self.assertGreater(F(result["minimum_atom"]), F(0))

    def test_group_specific_a_exact_n8(self):
        self.assert_block_exchange_exact_match(
            (F(1, 5), F(3, 4)),
            ((F(2, 5), F(1, 20)), (F(1, 20), F(3, 5))),
            (4, 4),
        )

    def test_group_specific_a_near_boundary_exact_n8(self):
        self.assert_block_exchange_exact_match(
            (F(1, 100), F(99, 100)),
            ((F(1, 50), F(1, 1000)), (F(1, 1000), F(49, 50))),
            (4, 4),
        )


if __name__ == "__main__":
    unittest.main()
