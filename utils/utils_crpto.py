import math

from Crypto import Random
from Crypto.PublicKey import ElGamal


class UtilsCrpto:

    @staticmethod
    def bytes_to_int(num):
        return int.from_bytes(num, byteorder='big')

    @staticmethod
    def int_to_bytes(num):
        # 将整数转换为字节串
        byte_length = (num.bit_length() + 7) // 8  # 计算字节长度
        byte_array = num.to_bytes(byte_length, byteorder='big')  # 转换为字节串
        return byte_array

    @staticmethod
    def construct_public_parametor(bitlen):
        """
        Construct generator and prime
        Args:
            bitlen(int): lenth of the generator and prime
        Returns:
            generator(int)
            prime(int)
        """
        key_pair = ElGamal.generate(bitlen, randfunc=Random.get_random_bytes)
        return int(key_pair.g), int(key_pair.p)

    @staticmethod
    def generate_key_pair(bitlen, g, p):
        """
        generate public key and private key
        Args:
            bitlen(int): lenth of the generator and prime
            g(int): generator
            p(int): prime
        Returns:
            pri_key(int)
            pub_key(int)
        """
        byteslen = int(bitlen / 8)
        random_bytes = Random.get_random_bytes(byteslen)
        random_int = UtilsCrpto.bytes_to_int(random_bytes)
        pri_key = random_int % p
        pub_key = pow(g, pri_key, p)
        return pri_key, pub_key

    @staticmethod
    def prime_factors(n):
        """
        get the smallest factors of the n
        Args:
            n(int): prime number
        Returns:
            factors(int): the smallest factors
        """
        factors = []
        while n % 2 == 0:
            return 2
            n //= 2
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            while n % i == 0:
                return i
        return factors
