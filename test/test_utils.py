import unittest

from Crypto.Util.number import isPrime

from utils import utils


def reverse_binary_string(binary_string):
    return binary_string[::-1]


class UtilsCrptoTest(unittest.TestCase):
    def test_int_to_bit_array_and_bit_array_to_int(self):
        bid = 52234
        max_length = 32
        bitarray = utils.int_to_bit_array(bid, max_length)
        num = utils.bit_array_to_int(bitarray)
        print(num)
        assert bid == num, "bid not equals to num"

    def test_pedersen_params(self):
        p, q, g, h = utils.generate_pedersen_params(32)
        # 检查p和q是否为素数
        assert isPrime(p), "p must be prime"
        assert isPrime(q), "q must be prime"

        # 检查q是否整除p-1
        assert (p - 1) % q == 0, "q must divide p-1"

        # 检查g是否为Z*p的生成元
        assert pow(g, q, p) == 1, "g must be a generator of Z*p of order q"

        # 检查h是否为g的高阶元素
        # 这里我们不能真的检查h的离散对数，因为它是未知的
        # 但我们可以检查h是否不等于1，这是一个简单的检查
        assert h != 1, "h must not be 1"

        print("test_pedersen_params passed!")


if __name__ == "__main__":
    unittest.main()
    # test_pedersen_params()
