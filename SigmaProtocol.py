import random

from Crypto.Hash import SHA256
from sympy import mod_inverse


class BV_Proof:
    def __init__(self, g, h, p, v, c, x_upper, y_upper, gamma1, gamma2, r1, r2, r3, r4, r5):
        self.g = g
        self.h = h
        self.p = p
        self.v = v
        self.c = c
        self.x_upper = x_upper
        self.y_upper = y_upper
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.r5 = r5


class AV_Proof:
    def __init__(self, g, h, p, v, c, x_upper, y_upper, y_upper_last, x_upper_last, l_gamma, l_r, d):
        self.g = g
        self.h = h
        self.p = p
        self.v = v
        self.c = c
        self.x_upper = x_upper
        self.y_upper = y_upper
        self.x_upper_last = x_upper_last
        self.y_upper_last = y_upper_last
        self.l_gamma = l_gamma
        self.l_r = l_r
        self.d = d


class SigmaProtocol:

    @staticmethod
    def generate_proof_BV(g, q, p, h, c, v, y_upper, x_upper, rir, xir, b, rr):
        alpha = 1
        if b == 1:
            alpha = 2
        # step 1, suppose alpha = 1
        l_v = []
        for i in range(4):
            l_v.append(random.randint(1, q))
        l_w = [0] * 2
        for i in range(2):
            if i + 1 == alpha:
                l_w[i] = 0
            else:
                l_w[i] = random.randint(1, q)

        t1 = (pow(c, l_w[0], p) * pow(h, l_v[0], p)) % p
        t2 = (pow(v, l_w[0], p) * pow(y_upper, l_v[1], p)) % p
        t3 = (pow(x_upper, l_w[0], p) * pow(g, l_v[1], p)) % p
        a = (c * mod_inverse(g, p)) % p
        t4 = (pow(a, l_w[1], p) * pow(h, l_v[2], p)) % p
        t5 = (pow(v, l_w[1], p) * pow(g, l_v[3], p)) % p
        # step 2
        merged_string = str(h) + str(c) + str(y_upper) + str(v) + str(g) + str(x_upper) + str(a) + str(t1) + str(
            t2) + str(t3) + str(t4) + str(t5)
        hash_hex = SHA256.new(merged_string.encode()).hexdigest()
        h_upper = int(hash_hex, 16) % p

        # step 3
        l_gamma = [0] * 2
        for i in range(2):
            if i + 1 == alpha:
                l_gamma[i] = (h_upper - l_w[0] - l_w[1]) % p
            else:
                l_gamma[i] = l_w[i]
        # gamma1 = (h_upper - l_w[0] - l_w[1]) % p
        # gamma2 = l_w[1]
        # step 4
        if alpha == 1:
            x1, x2, x3, x4 = rir, xir, 0, 0
        else:
            x1, x2, x3, x4 = 0, 0, rir, rr
        r1 = (l_v[0] - l_gamma[alpha - 1] * x1)
        r2 = (l_v[1] - l_gamma[alpha - 1] * x2)
        r3 = (l_v[1] - l_gamma[alpha - 1] * x2)
        r4 = (l_v[2] - l_gamma[alpha - 1] * x3)
        r5 = (l_v[3] - l_gamma[alpha - 1] * x4)
        return BV_Proof(g, h, p, v, c, x_upper, y_upper, l_gamma[0], l_gamma[1], r1, r2, r3, r4, r5)

    @staticmethod
    def check_proof_BV(g, h, p, v, c, x_upper, y_upper, gamma1, gamma2, r1, r2, r3, r4, r5):
        a = (c * mod_inverse(g, p)) % p
        # re-constructing the commitments
        t1_new = (pow(c, gamma1, p) * pow(h, r1, p)) % p
        t2_new = (pow(v, gamma1, p) * pow(y_upper, r2, p)) % p
        t3_new = (pow(x_upper, gamma1, p) * pow(g, r3, p)) % p
        t4_new = (pow(a, gamma2, p) * pow(h, r4, p)) % p
        t5_new = (pow(v, gamma2, p) * pow(g, r5, p)) % p

        # compute hash value
        # step 2
        merged_string = str(h) + str(c) + str(y_upper) + str(v) + str(g) + str(x_upper) + str(a) + str(t1_new) + str(
            t2_new) + str(t3_new) + str(t4_new) + str(t5_new)
        hash_hex = SHA256.new(merged_string.encode()).hexdigest()
        h_upper = int(hash_hex, 16) % p
        # check
        if (gamma1 + gamma2) % p == h_upper:
            return True
        else:
            return False

    @staticmethod
    def generate_proof_AV(g, q, p, h, c, v, y_upper, x_upper, y_upper_last, x_upper_last, rir, rir_overline,
                          rir_overline_last, xir, xir_last, b,
                          d):
        alpha = 0
        if b == 0:
            alpha = 1
        elif b == 1 and d == 1:
            alpha = 2
        else:
            alpha = 3

        l_v = []
        for i in range(8):
            l_v.append(random.randint(1, p))
        l_w = [0] * 3
        for i in range(3):
            if i + 1 == alpha:
                l_w[i] = 0
            else:
                l_w[i] = random.randint(1, p)
        l_t = [0] * 11
        l_t[0] = (pow(c, l_w[0], p) * pow(h, l_v[0], p)) % p
        l_t[1] = (pow(v, l_w[0], p) * pow(y_upper, l_v[1], p)) % p
        l_t[2] = (pow(x_upper, l_w[0], p) * pow(g, l_v[1], p)) % p  # t3
        a = (c * mod_inverse(g, p)) % p
        l_t[3] = (pow(a, l_w[1], p) * pow(h, l_v[2], p)) % p
        l_t[4] = (pow(d, l_w[1], p) * pow(g, l_v[3], p)) % p
        l_t[5] = (pow(v, l_w[1], p) * pow(g, l_v[4], p)) % p
        l_t[6] = (pow(a, l_w[2], p) * pow(h, l_v[5], p)) % p  # t7
        l_t[7] = (pow(d, l_w[2], p) * pow(y_upper_last, l_v[6], p)) % p  # t8
        l_t[8] = (pow(x_upper_last, l_w[2], p) * pow(g, l_v[6], p)) % p  # t9
        l_t[9] = (pow(v, l_w[2], p) * pow(y_upper, l_v[7], p)) % p  # t10
        l_t[10] = (pow(x_upper, l_w[2], p) * pow(g, l_v[7], p)) % p  # 11

        # compute hash value
        # step 2
        merged_string = str(h) + str(c) + str(y_upper) + str(v) + str(g) + str(x_upper) + str(a) + str(d) + str(
            y_upper_last) + str(x_upper_last) + str(l_t[0]) + str(l_t[1]) + str(l_t[2]) + str(l_t[3]) + str(
            l_t[4]) + str(l_t[5]) + str(l_t[6]) + \
                        str(l_t[7]) + str(l_t[8]) + str(l_t[9]) + str(l_t[10])
        hash_hex = SHA256.new(merged_string.encode()).hexdigest()
        h_upper = int(hash_hex, 16) % p

        # step 3: compute gamma
        l_gamma = [0] * 3
        for i in range(3):
            if i + 1 == alpha:
                l_gamma[i] = (h_upper - l_w[0] - l_w[1] - l_w[2]) % p
            else:
                l_gamma[i] = l_w[i]

        # step 4: compute R
        if alpha == 1:
            x1, x2, x3, x4, x5, x6, x7, x8 = rir, xir, 0, 0, 0, 0, 0, 0
        elif alpha == 2:
            x1, x2, x3, x4, x5, x6, x7, x8 = 0, 0, rir, rir_overline_last, rir_overline, 0, 0, 0
        else:
            x1, x2, x3, x4, x5, x6, x7, x8 = 0, 0, 0, 0, 0, rir, xir_last, xir
        l_r = [0] * 11
        l_r[0] = (l_v[0] - l_gamma[alpha - 1] * x1)
        l_r[1] = (l_v[1] - l_gamma[alpha - 1] * x2)  # r2
        l_r[2] = (l_v[1] - l_gamma[alpha - 1] * x2)  # r3

        # l_r[2] = mod_inverse(l_r[2], p)

        l_r[3] = (l_v[2] - l_gamma[alpha - 1] * x3)
        l_r[4] = (l_v[3] - l_gamma[alpha - 1] * x4)
        l_r[5] = (l_v[4] - l_gamma[alpha - 1] * x5)
        l_r[6] = (l_v[5] - l_gamma[alpha - 1] * x6)
        l_r[7] = (l_v[6] - l_gamma[alpha - 1] * x7)
        l_r[8] = (l_v[6] - l_gamma[alpha - 1] * x7)
        l_r[9] = (l_v[7] - l_gamma[alpha - 1] * x8)
        l_r[10] = (l_v[7] - l_gamma[alpha - 1] * x8)

        return AV_Proof(g, h, p, v, c, x_upper, y_upper, y_upper_last, x_upper_last, l_gamma, l_r, d)

    @staticmethod
    def check_proof_AV(g, h, p, v, c, x_upper, y_upper, y_upper_last, x_upper_last, l_gamma, l_r, d):
        a = (c * mod_inverse(g, p)) % p
        # re-constructing the commitments
        t1_new = (pow(c, l_gamma[0], p) * pow(h, l_r[0], p)) % p
        t2_new = (pow(v, l_gamma[0], p) * pow(y_upper, l_r[1], p)) % p
        print("x_upper", x_upper)
        print("gamma1", l_gamma[0])
        print("g", g)
        print("r3", l_r[2])
        t3_new = (pow(x_upper, l_gamma[0], p) * pow(g, l_r[2], p)) % p
        t4_new = (pow(a, l_gamma[1], p) * pow(h, l_r[3], p)) % p
        t5_new = (pow(d, l_gamma[1], p) * pow(g, l_r[4], p)) % p
        t6_new = (pow(v, l_gamma[1], p) * pow(g, l_r[5], p)) % p
        t7_new = (pow(a, l_gamma[2], p) * pow(h, l_r[6], p)) % p
        t8_new = (pow(d, l_gamma[2], p) * pow(y_upper_last, l_r[7], p)) % p
        t9_new = (pow(x_upper_last, l_gamma[2], p) * pow(g, l_r[8], p)) % p
        t10_new = (pow(v, l_gamma[2], p) * pow(y_upper, l_r[9], p)) % p
        t11_new = (pow(x_upper, l_gamma[2], p) * pow(g, l_r[10], p)) % p

        # compute hash value
        # step 2
        merged_string = str(h) + str(c) + str(y_upper) + str(v) + str(g) + str(x_upper) + str(a) + str(d) + str(
            y_upper_last) + str(x_upper_last) + str(t1_new) + str(t2_new) + str(t3_new) + str(t4_new) + str(
            t5_new) + str(t6_new) + str(t7_new) + \
                        str(t8_new) + str(t9_new) + str(t10_new) + str(t11_new)
        hash_hex = SHA256.new(merged_string.encode()).hexdigest()
        h_upper = int(hash_hex, 16) % p

        # check
        if (l_gamma[0] + l_gamma[1] + l_gamma[2]) % p == h_upper:
            return True
        else:
            return False
