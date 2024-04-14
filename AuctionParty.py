import random

from AnonymousVeto import AnonymousVeto
from Interaction_SC.AuctionSC import AuctionSC
from PVSS import PVSS
from SigmaProtocol import SigmaProtocol
from UTXO import Transaction
from utils import utils
from utils.utils_crpto import UtilsCrpto


class AuctionParty():
    def __init__(self, pid, bid, max_length, n, g=0, h=0, q=0, p=0):

        self.pid = pid  # identity of the auction party
        self.bid = bid
        self.max_length = max_length  # bits length of bid
        # binary_bid = bin(bid)[2:]
        self.l = max_length
        self.bir = utils.int_to_bit_array(bid, self.l)
        self.bi = bid
        self.n = n  # number of auction party
        # contract
        self.anvil_rpc = 'http://127.0.0.1:8545'
        self.contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
        self.abi_file = 'Interaction_SC/Auction.json'
        self.private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
        self.contract = AuctionSC(self.anvil_rpc, self.contract_address, self.abi_file, self.private_key)
        # receive from sc
        self.pbk_list = []  # public key of committee parties
        self.g = g
        self.h = h
        self.q = q
        self.p = p
        self.committee_count = 0
        self.cir = []
        self.rir = []
        self.l_xir = [None] * (max_length + 1)
        self.l_x_upper = [None] * (max_length + 1)
        self.l_y_upper = [None] * (max_length + 1)
        self.l_r_overline = [None] * (max_length + 1)
        self.dir = 1
        self.ci = None  # commitment
        self.tx = None  # transaction
        self.encrypted_shares = None
        self.LDEI_proof = None
        self.rbi = None

    def get_prime_from_smart_contract(self):
        p, q = self.contract.call_get_prime()
        self.p = UtilsCrpto.bytes_to_int(p)
        self.q = UtilsCrpto.bytes_to_int(q)

    def get_committee_count_from_smart_contract(self):
        self.committee_count = self.contract.call_get_committee_count()

    def get_param_from_smart_contract(self):
        g, h, pkl = self.contract.call_get_param()
        self.g = UtilsCrpto.bytes_to_int(g)
        self.h = UtilsCrpto.bytes_to_int(h)
        for i in range(0, self.n + 1):
            self.pbk_list.append(UtilsCrpto.bytes_to_int(pkl[i]))

    def stage1_setup(self):
        # 实现协议的stage1的Setup阶段
        # 1. 发送消息给SC，接收返回的参数
        self.get_committee_count_from_smart_contract()
        self.get_prime_from_smart_contract()
        self.get_param_from_smart_contract()
        # 2. 计算承诺
        self.cir, self.ci, self.rbi, self.rir = self._compute_commitment()
        # 3. create transaction
        self.tx = Transaction(random.randint(1, 256), self.ci, self.contract_address)
        # 4. 计算PVSS
        secrets = [pow(self.g, self.bi, self.p), pow(self.h, self.rbi, self.p)]

        n_secrete = 2
        self.encrypted_shares, self.LDEI_proof = PVSS.create_PVSS_shares(self.p, self.committee_count, n_secrete,
                                                                         secrets,
                                                                         self.pbk_list[1:])

        # result = PVSS.verify_LDEI(self.pbk_list[1:], self.p, proof.x_arr, proof.a_arr, self.committee_count,
        #                           proof.e,
        #                           proof.z_arr)
        return self.pbk_list[1:], self.encrypted_shares, self.LDEI_proof, self.tx

    def stage1_send_setup_to_smart_contract(self):
        tx_id = random.randint(1, 256)
        self.contract.send_setup(self.pid, tx_id, self.ci)

    def stage1_broadcast(self):
        for i in range(1, self.max_length + 1):
            self.l_xir[i], self.l_x_upper[i] = AnonymousVeto.broadcast(self.g, self.q, self.p)
        return self.l_xir, self.l_x_upper

    def stage1_compute_parameters_from_others(self, r, l_x):
        self.l_y_upper[r] = AnonymousVeto.compute_parameters_from_others(l_x, self.committee_count, self.pid,
                                                                         self.p)

    def stage2_before_first_veto(self, r):
        vir, rr = AnonymousVeto.compute_anonymous_veto(self.l_xir[r], self.l_y_upper[r], self.bir[r], self.g, self.q,
                                                       self.p)
        BV_proof = SigmaProtocol.generate_proof_BV(self.g, self.q, self.p, self.h, self.cir[r], vir,
                                                   self.l_y_upper[r], self.l_x_upper[r],
                                                   self.rir[r],
                                                   self.l_xir[r],
                                                   self.bir[r],
                                                   rr)
        self.l_r_overline[r] = rr
        return vir, rr, BV_proof

    def stage2_compute_before_first_veto(self, r, l_v, BV_proof_list):
        for proof in BV_proof_list:
            t = SigmaProtocol.check_proof_BV(proof.g, proof.h, proof.p, proof.v, proof.c, proof.x_upper, proof.y_upper,
                                             proof.gamma1, proof.gamma2,
                                             proof.r1, proof.r2, proof.r3, proof.r4, proof.r5)

            if not t:
                return None, False
        result = AnonymousVeto.compute_veto_result(l_v, self.committee_count, self.p)
        print(self.pid)
        if result == 1 and self.bir[r] == 0:
            self.dir = 0
        return result, True

    def stage2_after_first_veto(self, r, last_veto_round):
        if self.dir == 0:
            vir, rr = AnonymousVeto.compute_anonymous_veto_after_first_veto(self.l_xir[r], self.l_y_upper[r], self.p)
        else:
            vir, rr = AnonymousVeto.compute_anonymous_veto(self.l_xir[r], self.l_y_upper[r], self.bir[r], self.g,
                                                           self.q,
                                                           self.p)

        self.l_r_overline[r] = rr
        av_proof = SigmaProtocol.generate_proof_AV(self.g, self.q, self.p, self.h, self.cir[r], vir,
                                                   self.l_y_upper[r],
                                                   self.l_x_upper[r],
                                                   self.l_y_upper[last_veto_round],
                                                   self.l_x_upper[last_veto_round], self.rir[r],
                                                   rr,
                                                   self.l_r_overline[last_veto_round], self.l_xir[r],
                                                   self.l_xir[last_veto_round],
                                                   self.bir[r],
                                                   self.dir)
        return vir, rr, av_proof

    def stage2_compute_after_first_veto(self, r, l_v, av_proof_list):
        for proof in av_proof_list:
            t = SigmaProtocol.check_proof_AV(proof.g, proof.h, proof.p, proof.v, proof.c, proof.x_upper,
                                             proof.y_upper, proof.y_upper_last,
                                             proof.x_upper_last, proof.l_gamma, proof.l_r, proof.d)

            if not t:
                return AnonymousVeto.compute_veto_result(l_v, self.committee_count, self.p), False
        result = AnonymousVeto.compute_veto_result(l_v, self.committee_count, self.p)
        if result == 1 and self.bir[r] == 0:
            self.dir = 0
        return result, True

    # Pi sample xir<-zq, and compute Xir = g^xir
    def _anonymous_veto_setup(self):
        xir = []
        Xir = []
        for i in range(self.l):
            v = random.randint(1, self.q)
            xir.append(v)
            Xir.append(pow(self.g, v, self.q))
        return xir, Xir

    # # Upon receiving all message cji and Xji, Pi computes Yjk
    # def _anonymous_veto_compute_Y(self, Cjl, Xjl):
    #     Yjk = []
    #     for k in range(1, self.l):
    #         Yjk[k] = 1
    #         for m in range(1, self.n):
    #             if m
    #             Yjk[k] = Yjk[k]
    def _compute_commitment(self):
        # list rir cir
        rir = [0] * (self.l + 1)
        assert self.q > 1, "q <=1 "
        for i in range(1, self.l + 1):
            rir[i] = random.randint(1, self.q)

        cir = [0] * (self.l + 1)
        for i in range(1, self.l + 1):
            cir[i] = (pow(self.g, self.bir[i], self.p) * pow(self.h, rir[i], self.p)) % self.p

        # bid commitment ci
        ci = 1
        for r in range(1, self.l + 1):
            ci = (ci * pow(cir[r], pow(2, self.l - r, self.p), self.p)) % self.p
        # ci can be rewritten to
        rbi = 0
        for r in range(1, self.l + 1):
            rbi = rbi + pow(2, self.l - r, self.p) * rir[r]

        ci_check = pow(self.g, self.bi, self.p) * pow(self.h, rbi, self.p) % self.p

        assert ci_check == ci, "Commitment Compute error"
        return cir, ci, rbi, rir

    def stage4_open_commitment(self, win_bid):
        if win_bid == self.bid:
            self.contract.send_openCommitment(self.pid, self.bid, self.rbi)
