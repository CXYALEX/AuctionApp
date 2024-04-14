import unittest

from AuctionParty import AuctionParty  # 替换为您的模块名


class TestAuctionParty(unittest.TestCase):
    def setUp(self):
        # 初始化测试用例
        self.party = AuctionParty(
            pid=1,
            bid=35,
            g=7698,
            h=7094,
            p=7703,
            q=3851,
            max_length=12,
            n=5
        )

    def test_compute_commitment(self):
        # 测试位承诺计算
        ci = self.party._compute_commitment()

    def test_anonymous_veto_setup(self):
        xir, Xir = self.party._anonymous_veto_setup()

        self.assertEqual(len(xir), self.party.l)
        self.assertEqual(len(Xir), self.party.l)
        for i in range(self.party.l):
            self.assertGreaterEqual(xir[i], 1)
            self.assertLessEqual(xir[i], self.party.q)
            self.assertEqual(Xir[i], pow(self.party.g, xir[i], self.party.q))


if __name__ == "__main__":
    unittest.main()
