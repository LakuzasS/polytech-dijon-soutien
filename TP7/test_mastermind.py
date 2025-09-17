import unittest
import os
import tempfile

from TP7.mastermind import Mastermind, Stats


class TestMastermind(unittest.TestCase):
    def test_generercode_length_and_values(self):
        couleurs = ['R', 'G', 'B', 'Y']
        m = Mastermind(couleurs, 4, 12)
        code = m.generercode()
        self.assertEqual(len(code), 4)
        for c in code:
            self.assertIn(c, couleurs)

    def test_verifessai_all_correct(self):
        couleurs = ['R', 'G', 'B', 'Y']
        m = Mastermind(couleurs, 4, 12)
        m.codesecret = ['R', 'G', 'B', 'Y']
        bon, mauvais = m.verifessai(['R', 'G', 'B', 'Y'])
        self.assertEqual((bon, mauvais), (4, 0))

    def test_verifessai_partial_and_correct(self):
        couleurs = ['R', 'G', 'B', 'Y']
        m = Mastermind(couleurs, 4, 12)
        m.codesecret = ['R', 'R', 'G', 'B']
        bon, mauvais = m.verifessai(['R', 'G', 'R', 'B'])
        self.assertEqual((bon, mauvais), (2, 2))


class TestStats(unittest.TestCase):
    def test_stats_add_and_reset(self):
        fd, path = tempfile.mkstemp(prefix='mm_stats_test_', dir='.')
        os.close(fd)
        try:
            s = Stats(path=path)
            # reset to known state
            s.reset()
            data = s.lire()
            self.assertEqual(data.get('nb_parties'), 0)
            self.assertEqual(data.get('score_total'), 0)

            new = s.ajouter(5)
            self.assertEqual(new.get('nb_parties'), 1)
            self.assertEqual(new.get('score_total'), 5)

            new2 = s.ajouter(3)
            self.assertEqual(new2.get('nb_parties'), 2)
            self.assertEqual(new2.get('score_total'), 8)

            s.reset()
            data2 = s.lire()
            self.assertEqual(data2.get('nb_parties'), 0)
            self.assertEqual(data2.get('score_total'), 0)
        finally:
            try:
                os.remove(path)
            except Exception:
                pass


if __name__ == '__main__':
    unittest.main()
