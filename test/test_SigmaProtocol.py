import time
import unittest

from SigmaProtocol import SigmaProtocol


class SigmaProtocolTest(unittest.TestCase):
    def test_process_BV(self):
        start_time = time.time()
        test_cases = [
            {"g": 2, "q": 17, "p": 3851, "h": 3, "c": 617673396283947,
             "v": 5843211045545439551605946764725979847,
             "y_upper": 23, "x_upper": 134217728, "r": 31, "x": 27, "b": 0, "rr": 7},
            {"g": 2, "q": 17, "p": 3851, "h": 3, "c": 856,
             "v": 2163,
             "y_upper": 23, "x_upper": 134217728, "r": 31, "x": 27, "b": 1, "rr": 37}
        ]
        for test_case in test_cases:
            g = test_case["g"]
            q = test_case["q"]
            p = test_case["p"]
            h = test_case["h"]
            c = test_case["c"]
            v = test_case["v"]
            y_upper = test_case["y_upper"]
            x_upper = test_case["x_upper"]
            rir = test_case["r"]
            xir = test_case["x"]
            b = test_case["b"]
            rr = test_case["rr"]
            BV_Proof = SigmaProtocol.generate_proof_BV(g, q,
                                                       p,
                                                       h, c,
                                                       v,
                                                       y_upper,
                                                       x_upper,
                                                       rir,
                                                       xir,
                                                       b, rr)
            res = SigmaProtocol.check_proof_BV(BV_Proof.g, BV_Proof.h, BV_Proof.p, BV_Proof.v, BV_Proof.c,
                                               BV_Proof.x_upper, BV_Proof.y_upper, BV_Proof.gamma1, BV_Proof.gamma2,
                                               BV_Proof.r1, BV_Proof.r2, BV_Proof.r3, BV_Proof.r4,
                                               BV_Proof.r5)
            self.assertTrue(res)
        end_time = time.time()
        execution_time = (end_time - start_time) / len(test_cases)
        print(f"execution_time：{execution_time} s")

    def test_process_AV(self):
        start_time = time.time()
        test_cases = [
            {"g": 2, "q": 17, "p": 3851, "h": 3, "rir": 21, "c": 1284, "xir": 47, "x_upper": 587, "y_upper": 311,
             "v": 3509, "x_upper_last": 34, "y_upper_last": 31, "b": 0, "d": 1, "xir_last": 11, "rir_overline_last": 31,
             "rir_overline": 17},
            {"g": 2, "q": 17, "p": 3851, "h": 3, "rir": 21, "c": 2568, "xir": 47, "x_upper": 587, "y_upper": 311,
             "v": 138, "x_upper_last": 34, "y_upper_last": 31, "b": 1, "d": 1, "xir_last": 11, "rir_overline_last": 0,
             "rir_overline": 17}
            # {"g": 2, "q": 17, "p": 3851, "h": 3, "rir": 21, "c": 1284, "xir": 47, "x_upper": 587, "y_upper": 311,
            #  "v": 3509, "x_upper_last": 34, "y_upper_last": 31, "b": 1, "d": 0, "xir_last": 11, "rir_overline_last": 31,
            #  "rir_overline": 17}
        ]
        for test_case in test_cases:
            g = test_case["g"]
            q = test_case["q"]
            p = test_case["p"]
            h = test_case["h"]
            c = test_case["c"]
            v = test_case["v"]
            y_upper = test_case["y_upper"]
            x_upper = test_case["x_upper"]
            y_upper_last = test_case["y_upper_last"]
            x_upper_last = test_case["x_upper_last"]
            rir = test_case["rir"]
            b = test_case["b"]
            d = test_case["d"]
            xir = test_case["xir"]
            xir_last = test_case["xir_last"]
            rir_overline = test_case["rir_overline"]
            rir_overline_last = test_case["rir_overline_last"]
            av_proof = SigmaProtocol.generate_proof_AV(
                g, q, p, h, c, v, y_upper, x_upper, y_upper_last, x_upper_last, rir, rir_overline,
                rir_overline_last, xir, xir_last, b,
                d)
            res = SigmaProtocol.check_proof_AV(g, h, p, v, c, x_upper, y_upper, y_upper_last, x_upper_last,
                                               av_proof.l_gamma,
                                               av_proof.l_r, d)
            self.assertTrue(res)
        end_time = time.time()
        execution_time = (end_time - start_time) / len(test_cases)
        print(f"execution_time：{execution_time} s")


if __name__ == '__main__':
    unittest.main()
