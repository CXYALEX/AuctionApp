import unittest

from AnonymousVeto import AnonymousVeto


class AnonymousVetoTestCase(unittest.TestCase):

    def test_complete_process(self):
        test_cases = [
            {"g": 2, "q": 23,
             "p": 9636706478826078902464349245931,
             "bid": [0, 0, 0], "n": 3, "output": 0},

            {"g": 8947659721587504322369235589080067732472617341483821918081839005310054682019, "q": 17,
             "p": 96367064788260789024643492459309671310989994637267112636540218393740380697799,
             "bid": [0, 0, 0], "n": 3, "output": 0},
            {"g": 2, "q": 23, "p": 3851, "bid": [0, 0, 0, 0], "n": 4, "output": 0},
            {"g": 2, "q": 17, "p": 3851, "bid": [0, 0, 0, 1, 1], "n": 5, "output": 1},
            {"g": 2, "q": 17, "p": 3851, "bid": [1, 1, 0, 1, 1], "n": 5, "output": 1},
        ]
        for test_case in test_cases:
            print("testcase:", test_case)
            g = test_case["g"]
            q = test_case["q"]
            p = test_case["p"]
            bid = test_case["bid"]
            n = test_case["n"]
            self.assertEqual(len(bid), n)
            lx = []
            lx_secret = []
            for i in range(n):
                x_secret, x = AnonymousVeto.broadcast(g, q, p)
                lx_secret.append(x_secret)
                lx.append(x)
            print("lx", lx)
            print("lx_secret", lx_secret)

            yv = []
            for i in range(1, n + 1):
                yv.append(AnonymousVeto.compute_parameters_from_others(lx, n, i, p))
            print("yv", yv)

            lv = []
            for i in range(1, n + 1):
                v, r = AnonymousVeto.compute_anonymous_veto(lx_secret[i - 1], yv[i - 1], bid[i - 1], g, q, p)
                lv.append(v)
            res = AnonymousVeto.compute_veto_result(lv, n, p)

            print("res", res)
            self.assertEqual(test_case["output"], res)


if __name__ == '__main__':
    unittest.main()
