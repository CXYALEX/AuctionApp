import random

from sympy import mod_inverse


class AnonymousVeto:

    @staticmethod
    def broadcast(g, q, p):
        """
        randomly generate x, then send g^x to other parties
        Args:
            g: generator of G
            q: order of G
            p: big prime of G
        Returns:
            x: random secret
            pow(g,x,p): x_upper
        """
        x = random.randint(1, q - 1)
        return x, pow(g, x, p)

    @staticmethod
    def compute_parameters_from_others(l_x, n, id, p):
        """
            Upon receive g^xi from other parties, compute Yjk. Ref: https://www.dcs.warwick.ac.uk/~fenghao/files/av_net.pdf
            Args:
                l_x: g^x receive from other parties
                n: number of parties
                id: the id of the parties, id = 1,...n
                p: big prime of G
            Returns:
                y_value % p
        """
        assert len(l_x) == n, "len of X not equals to n"
        y_value = 1
        for i in range(1, n + 1):
            if i < id:
                y_value = y_value * l_x[i - 1] % p
            elif i > id:
                y_value = y_value * (mod_inverse(l_x[i - 1], p))
            else:
                continue
        return y_value % p

    @staticmethod
    def compute_anonymous_veto(x, Y, b, g, q, p):
        """
            compute vir
            Args:
                x: random secrete x
                Y:
                b: bid
                g: generator of G
                q: order of G
                p: big prime of G
            Returns:
                Y^x if b == 0 else Y^r,r=random()
        """
        v = 0
        r = 0
        if b == 0:
            v = pow(Y, x, p)
        else:
            r = random.randint(1, q - 1)
            v = pow(g, r, p)
        return v, r

    @staticmethod
    def compute_anonymous_veto_after_first_veto(x, Y, p):
        return pow(Y, x, p), 0

    @staticmethod
    def compute_veto_result(l_v, n, p):
        value = 1
        for i in range(n):
            if l_v[i] == None:
                continue
            value = value * l_v[i] % p
        if value == 1:
            return 0  # no veto
        else:
            return 1  # has veto

    @staticmethod
    def recompute_parameters_from_others_exclude_w(l_x, n, id, p,w):
        """
            Upon receive g^xi from other parties, compute Yjk. Ref: https://www.dcs.warwick.ac.uk/~fenghao/files/av_net.pdf
            Args:
                l_x: g^x receive from other parties
                n: number of parties
                id: the id of the parties, id = 1,...n
                p: big prime of G
                w: exluding P_w
            Returns:
                y_value % p
        """
        assert len(l_x) == n, "len of X not equals to n"
        y_value = 1
        for i in range(1, n + 1):
            if i == w:
                continue
            elif i < id:
                y_value = y_value * l_x[i - 1] % p
            elif i > id:
                y_value = y_value * (mod_inverse(l_x[i - 1], p))
            else:
                continue
        return y_value % p