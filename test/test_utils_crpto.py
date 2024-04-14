from utils.utils_crpto import UtilsCrpto

bitlen = 256

import unittest


class UtilsCrptoTest(unittest.TestCase):
    def test_bytes_to_int(self):
        num = 123412351235
        num = UtilsCrpto.int_to_bytes(num)
        result = UtilsCrpto.bytes_to_int(num)
        assert result == 123412351235, "bytes_to_int test failed"

    def test_generate_key_pair(self):
        g, p = UtilsCrpto.construct_public_parametor(bitlen)
        pri_key, pub_key = UtilsCrpto.generate_key_pair(bitlen, g, p)
        assert isinstance(pri_key, int) and isinstance(pub_key, int), "generate_key_pair test failed"


if __name__ == "__main__":
    unittest.main()
