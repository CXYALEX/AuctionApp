from utils.utils_crpto import UtilsCrpto


class PedersenCommitment:
    def __init__(self, p, q, g, h):
        self.p = p
        self.q = q
        self.g = g
        self.h = h

    def pedersen_commit(self, m, r):
        if m < 0 or m >= self.p:
            raise ValueError("Message is out of range")
        if r < 0 or r >= self.p:
            raise ValueError("Random number is out of range")

        c = pow(self.g, m, self.p) * pow(self.h, r, self.p) % self.p
        return c

    def pedersen_open(self, m, r, c):
        if m < 0 or m >= self.p:
            return False
        if r < 0 or r >= self.p:
            return False

        lhs = pow(self.g, m, self.p) * pow(self.h, r, self.p) % self.p
        rhs = c % self.p
        return lhs == rhs


if __name__ == '__main__':
    # 示例用法
    p = 7703
    q = 3851
    g = 7698
    h = 7094

    print("p", UtilsCrpto.int_to_bytes(p), "q", UtilsCrpto.int_to_bytes(q))
    print("g", UtilsCrpto.int_to_bytes(g), "h", UtilsCrpto.int_to_bytes(h))
    commitment = PedersenCommitment(7703, 3851, 7698, 7094)

    message = 42
    random_number = 10
    commitment_value = commitment.pedersen_commit(message, random_number)
    print("Commitment value:", commitment_value)
    print("Verification result:", commitment.pedersen_open(message, random_number, commitment_value))
