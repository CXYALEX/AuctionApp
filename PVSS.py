import math
import random

from Crypto.Hash import SHA256
from sympy import symbols, interpolate


# 传入的a, b是字符串
def multiply(a, b):
    """
        Args:
            a(string)
            b(string)
        Returns:
            a*b(string)
    """
    result = 0
    for i in range(len(a)):
        for j in range(len(b)):
            result += int(a[i]) * int(b[j]) * 10 ** (len(a) - i - 1 + len(b) - j - 1)
    return str(result)


class LDEI_Proof:
    def __init__(self, generators, p, x_arr, a_arr, m, e, z_arr):
        self.generator = generators
        self.p = p
        self.x_arr = x_arr
        self.a_arr = a_arr
        self.m = m
        self.e = e
        self.z_arr = z_arr

    def encode(self):
        s = ""
        for item in self.generator:
            s = s + str(item)
        return (s + str(self.p) + str(self.x_arr) + str(self.a_arr) + str(
            self.m) + str(self.e) + str(self.z_arr)).encode("utf-8")

    # Define the PVSS class


class PVSS:
    @staticmethod
    def create_shares(p, n, l, secrets):
        """
        The dealer compute the secret share
        Args:
            p: big prime
            n: number of party
            l: number of secret
            secrets(list): list of secrets
        Returns:
            shares(list): list of shares
        """
        # Distribution phase: The dealer samples a polynomial and sets secrets
        X = symbols('X')
        t = math.ceil(n / 2) - 1
        points = []
        for i in range(len(secrets)):
            points.append((-(i + 1), secrets[i]))
        for i in range(n - t - l):
            points.append((i + 1, random.randint(0, p - 1)))
        poly = interpolate(points, X)
        shares = []
        # print(points)
        for i in range(1, n + 1):
            shares.append((i, poly.subs(X, i) % p))
        return shares

    @staticmethod
    def create_encrypted_shares(p, n, l, secrets, pki):
        """
        The dealer compute the encrypted secret share
        Args:
            p: big prime
            n: number of party
            l: number of secret
            secrets(list): list of secrets
            pki(list): public key list from n parties
        Returns:
            shares(list): list of encrypted secret shares
        """
        shares = PVSS.create_shares(p, n, l, secrets)
        encrypted_shares = []
        for i in range(len(shares)):
            # 这里的取mod可能有问题？
            encrypted_shares.append(pow(pki[i], int(shares[i][1] % p), p))
        return encrypted_shares

    @staticmethod
    def construct_LDEI(generators, m, p, p_arr, x_arr):
        """
        Generate the Proof of LDEI: x1 = g1^p(alpha 1); x2 = g2^p(alpha 2)
        Args:
            generators: generator of group G, it can be pki of the committee
            m: the number of generator
            p: big prime of cyclic group G
            p_arr(list): witnesses
            x_arr(list): statements
        Returns:
            proof of LDEI
        """
        assert len(generators) == m, "the number of generators not equals to m"
        a_arr = []
        r_arr = [random.randint(1, p - 1) for _ in range(m)]
        for i in range(m):
            a_arr.append(pow(generators[i], r_arr[i], p))
        merged_string = ''.join(map(str, x_arr + a_arr))
        hash_hex = SHA256.new(merged_string.encode()).hexdigest()
        e = int(hash_hex, 16) % p % pow(2, 32)
        z_arr = []
        for i in range(m):
            z_arr.append(((e * p_arr[i] % p) + r_arr[i]) % p)
        return LDEI_Proof(generators, p, x_arr, a_arr, m, e, z_arr)

    @staticmethod
    def verify_LDEI(generators, p, x_arr, a_arr, m, e, z_arr):
        assert len(generators) == m, "the number of generators not equals to m"
        assert len(a_arr) == m, "the number of a array not equals to m"
        assert len(z_arr) == m, "the number of z array not equals to m"
        assert len(x_arr) == m, "the number of x array not equals to m"
        for i in range(m):
            lvalue = (pow(x_arr[i], e, p) * a_arr[i]) % p
            rvalue = pow(generators[i], int(z_arr[i]), p)
            # lvalue_new = ((pow(x_arr[i], e) % p) * a_arr[i]) % p
            # rvalue_new = pow(generators[i], (z_arr[i])) % p
            if lvalue != rvalue:
                # print("rvalue_new:", rvalue_new)
                return False
            # if (pow(x_arr[i], e, p) * a_arr[i]) % p != pow(generators[i], z_arr[i], p):
            #     return False
        return True

    @staticmethod
    def secret_reconstruction(n, l, shares, p):
        """
        Reconstruct secret if the number of shares is bigger than n/2 + 1
        Args:
            n: number of party
            l: number of secret
            shares(list): list of shares
        Returns:
            secrets(list): list of secrets, e.g. s1=poly(-1); s2=poly(-2)....
       """
        t = math.ceil(n / 2) - 1
        assert len(shares) >= (n - t), "the number of shares is too less to reconstruct secrets"
        X = symbols('X')
        poly = interpolate(shares, X)
        secrets = []
        for i in range(l):
            secrets.append((-(i + 1), poly.subs(X, -(i + 1)) % p))
        return secrets

    @staticmethod
    def create_PVSS_shares(p, n, l, secrets, pki):
        """
        The dealer compute the encrypted secret share
        Args:
            p: big prime
            n: number of party
            l: number of secret
            secrets(list): list of secrets
            pki(list): public key list from n parties
        Returns:
            shares(list): list of encrypted secret shares
            LDEI: LDEI proof
        """
        # shares = PVSS.create_shares(p, n, l, secrets)
        # encrypted_shares = []
        # for i in range(len(shares)):
        #     # 这里的取mod可能有问题？
        #     encrypted_shares.append(pow(pki[i], int(shares[i][1] % p), p))
        # return encrypted_shares

        shares = PVSS.create_shares(p, n, l, secrets)
        encrypted_shares = []

        p_arr = []
        for i in range(len(shares)):
            v = int(shares[i][1]) % p % pow(2, 128)  # pow(2^256,2^256,p) 不准，所以这里取了128位！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            p_arr.append(v)
            encrypted_shares.append(pow(pki[i], v, p))
            # p_arr.append(i + 113)
            # encrypted_shares.append(pow(pki[i], i + 113, p))

        proof = PVSS.construct_LDEI(pki, n, p, p_arr, encrypted_shares)
        return encrypted_shares, proof


if __name__ == '__main__':
    pvss = PVSS()
    secrets = [21341, 123442]
    shares = pvss.create_shares(4423212341234123412341, 8, 2, secrets)
    pki = [2, 3, 5, 7, 11, 13, 17, 23]
    encrypted_shares = pvss.create_encrypted_shares(4423212341234123412341, 8, 2, secrets, pki)
    s = pvss.secret_reconstruction(8, 2, shares, 4423212341234123412341)
