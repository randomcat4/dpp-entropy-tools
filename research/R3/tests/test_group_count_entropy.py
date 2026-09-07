from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "artifacts" / "group_count_entropy.py"
SPEC = importlib.util.spec_from_file_location("group_count_entropy", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class GroupCountEntropyTests(unittest.TestCase):
    def test_direct_mobius_matches_count_reduction(self) -> None:
        result = MODULE.run_self_test()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(len(result["cases"]), 3)

    def test_orbit_sizes_cover_all_subsets(self) -> None:
        sizes = [2, 3, 2]
        rows = MODULE.group_count_table(
            sizes,
            [0.2, 0.5, 0.8],
            [[0.3, 0.02, 0.01], [0.02, 0.55, -0.03], [0.01, -0.03, 0.75]],
        )
        self.assertEqual(sum(row.multiplicity for row in rows), 2 ** sum(sizes))

    def test_rejects_noncontractive_group_matrix(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.grouped_entropy([2, 2], [0.2, 0.7], [[0.5, 0.8], [0.8, 0.5]])


if __name__ == "__main__":
    unittest.main()
