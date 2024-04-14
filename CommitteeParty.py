from hashlib import sha256

from Interaction_SC.AuctionSC import AuctionSC
from PVSS import PVSS
from utils.utils_crpto import UtilsCrpto


class CommitteeParty:
    def __init__(self, sid, bitlen, g, p):
        self.sid = sid
        self.p = p
        self.g = g
        self.pri_key, self.pub_key = UtilsCrpto.generate_key_pair(bitlen, g, p)
        # contract
        self.anvil_rpc = 'http://127.0.0.1:8545'
        self.contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
        self.abi_file = 'Interaction_SC/Auction.json'
        self.private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
        self.contract = AuctionSC(self.anvil_rpc, self.contract_address, self.abi_file, self.private_key)

    def upload_pk_to_smart_contract(self):
        pk = UtilsCrpto.int_to_bytes(self.pub_key)
        self.contract.send_set_pkcList(self.sid, pk)

    def setup_verification(self, tx, pki, n, encrypted_shares, LDEI_proof):
        # Verify shares correctness with LDEI
        if not self._verify_shares_correctness_with_LDEI(n, pki, LDEI_proof):
            return False, None

        # Verify NIZK CC

        # Compute hashes
        sh1i = sha256(tx.encode() + str(pki).encode()).digest()
        sh2i = sha256(LDEI_proof.encode()).digest()

        # Sign the hashes
        signature = self._sign_hash(sh1i + sh2i)

        return True, signature

    def _verify_shares_correctness_with_LDEI(self, n, pki, proof):
        return PVSS.verify_LDEI(pki, self.p, proof.x_arr, proof.a_arr, n,
                                proof.e,
                                proof.z_arr)

    def _sign_hash(self, hash):
        # key = RSA.construct(self.pri_key)
        # signer = pkcs1_15.new(key)
        # signature = signer.sign(SHA256.new(hash))
        #
        # return signature
        return hash

    def _decrypt_share(self, share):
        # Decrypt the share
        # Implement your own decryption logic here
        return share


if __name__ == '__main__':
    print("hello")
