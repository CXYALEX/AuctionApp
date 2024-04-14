import unittest

from AuctionSC import AuctionSC


class TestAuctionSC(unittest.TestCase):
    def setUp(self):
        self.anvil_rpc = 'http://127.0.0.1:8545'
        self.contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
        self.abi_file = 'Auction.json'
        self.private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
        self.contract = AuctionSC(self.anvil_rpc, self.contract_address, self.abi_file, self.private_key)

    def test_get_balance(self):
        balance = self.contract.get_balance()
        self.assertIsNotNone(balance)

    def test_send_set_generator(self):
        g = 8
        h = 10
        g = g.to_bytes()
        h = h.to_bytes()
        self.contract.send_set_generator(g, h)
        # Add assertions here

    def test_send_set_pkcList(self):
        index = 1
        big_int = 1234567890123456789012345678901234567890  # 要转换的大整数
        byte_length = (big_int.bit_length() + 7) // 8  # 根据大整数的位数计算所需的字节长度
        byte_order = 'big'  # 字节顺序，'big'表示高位字节在前，'little'表示低位字节在前

        pk = big_int.to_bytes(byte_length, byte_order)
        self.contract.send_set_pkcList(index, pk)
        # Add assertions here

    def test_call_get_generator(self):
        result = self.contract.call_get_generator()
        self.assertIsNotNone(result)

    def test_call_get_param(self):
        result = self.contract.call_get_param()
        print(result)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
