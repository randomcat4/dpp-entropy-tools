import unittest
from bridge_certificate import certify, graph_bridges


def make_case(n, edges, direction):
    K = [["1/2" if i == j else "0" for j in range(n)] for i in range(n)]
    A = [["0" for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        K[u][v] = K[v][u] = "1/20"
    for u, v in direction:
        A[u][v], A[v][u] = "1", "-1"
    return {'K': K, 'A': A}


class CertificateTests(unittest.TestCase):
    def test_nonzero_two_point(self):
        r = certify(make_case(2, [(0, 1)], [(0, 1)]))
        self.assertEqual(r['curvature_by_theorem'], 'STRICTLY_NEGATIVE')
        self.assertEqual(r['event_probabilities_evaluated'], 0)

    def test_tree_multiple_directions(self):
        r = certify(make_case(5, [(0,1),(1,2),(1,3),(3,4)], [(0,1),(1,3)]))
        self.assertEqual(r['curvature_by_theorem'], 'STRICTLY_NEGATIVE')

    def test_dense_blocks_with_bridge(self):
        edges=[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(2,3)]
        r=certify(make_case(6,edges,[(2,3)]))
        self.assertEqual(r['bridges_zero_based'], [(2,3)])
        self.assertEqual(r['curvature_by_theorem'], 'STRICTLY_NEGATIVE')

    def test_cycle_not_applicable(self):
        r=certify(make_case(3,[(0,1),(1,2),(0,2)],[(0,1)]))
        self.assertEqual(r['status'], 'NOT_APPLICABLE')

    def test_new_edge_not_applicable(self):
        r=certify(make_case(2,[],[(0,1)]))
        self.assertEqual(r['status'], 'NOT_APPLICABLE')

    def test_zero_and_disconnected(self):
        r=certify(make_case(4,[(0,1),(2,3)],[]))
        self.assertEqual(r['curvature_by_theorem'], 'ZERO')

    def test_boundary_invalid(self):
        self.assertEqual(certify({'K':[['1']], 'A':[['0']]})['status'], 'INVALID_INPUT')

    def test_asymmetric_invalid(self):
        p=make_case(2,[(0,1)],[(0,1)]);p['K'][0][1]='1/10'
        self.assertEqual(certify(p)['status'], 'INVALID_INPUT')

    def test_non_skew_invalid(self):
        p=make_case(2,[(0,1)],[(0,1)]);p['A'][1][0]='1'
        self.assertEqual(certify(p)['status'], 'INVALID_INPUT')

    def test_float_rejected(self):
        self.assertEqual(certify({'K':[[0.5]], 'A':[[0]]})['status'], 'INVALID_INPUT')

    def test_iterative_long_path(self):
        n=2000
        adjacency=[[j for j in (i-1,i+1) if 0<=j<n] for i in range(n)]
        self.assertEqual(len(graph_bridges(adjacency)), n-1)


if __name__ == '__main__':
    unittest.main()
