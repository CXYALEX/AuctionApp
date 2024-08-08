from pybulletproofs import zkrp_prove, zkrp_verify

class Rangeproof:
    def __init__(self, proof, commitment,range):
        self.proof = proof
        self.commitment = commitment
        self.range = range
    @staticmethod
    def generate_rangeproof(value,range):
        proof1, comm1, _ = zkrp_prove(value, range)
        return Rangeproof(proof1,comm1,range)
    @staticmethod
    def verify_rangeproof(Rangeproof):
        return zkrp_verify(Rangeproof.proof, Rangeproof.commitment,Rangeproof.range)

if __name__ == "__main__":
    proof = Rangeproof.generate_rangeproof(2147483649,32)
    print(Rangeproof.verify_rangeproof(proof))