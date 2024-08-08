import random

from AuctionParty import AuctionParty
from CommitteeParty import CommitteeParty
from Interaction_SC.AuctionSC import AuctionSC
from utils import utils
from utils.utils_crpto import UtilsCrpto

BIT_LEN = 256

if __name__ == "__main__":
    print("Auction Begin:")
    # prepare paremeters
    n = 3
    n_commitee = 3
    g, p = UtilsCrpto.construct_public_parametor(BIT_LEN)
    anvil_rpc = 'http://127.0.0.1:8545'
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    abi_file = 'Interaction_SC/Auction.json'
    private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
    contract = AuctionSC(anvil_rpc, contract_address, abi_file, private_key)
    # upload g,h to smart contract
    h = pow(g, random.randint(1, p), p)
    q = pow(g, random.randint(2, p), p) % pow(2, 32)
    bytes_g = UtilsCrpto.int_to_bytes(g)
    bytes_h = UtilsCrpto.int_to_bytes(h)
    bytes_p = UtilsCrpto.int_to_bytes(p)
    bytes_q = UtilsCrpto.int_to_bytes(q)
    contract.send_set_generator(bytes_g, bytes_h)
    contract.send_set_prime(bytes_p, bytes_q)
    # init committee parties
    committee_p1 = CommitteeParty(1, BIT_LEN, g, p)
    committee_p2 = CommitteeParty(2, BIT_LEN, g, p)
    committee_p3 = CommitteeParty(3, BIT_LEN, g, p)
    # upload pk to smart contract
    committee_p1.upload_pk_to_smart_contract()
    committee_p2.upload_pk_to_smart_contract()
    committee_p3.upload_pk_to_smart_contract()
    # init auction parties
    max_len = 32
    # auction_p1 = AuctionParty(1, 5 + pow(2, 31), max_len, 3)
    auction_p1 = AuctionParty(1, 25311, max_len, 3)
    auction_p2 = AuctionParty(2, 12431151, max_len, 3)
    auction_p3 = AuctionParty(3, 13431231, max_len, 3)
    # auction parties stage1 sutup
    encrypted_shares = [None] * (n + 1)
    LDEI_proof = [None] * (n + 1)
    pk_list_committee = [None] * (n + 1)
    rangeproof = [None] * (n + 1)
    pk_list_committee[1], encrypted_shares[1], LDEI_proof[1], tx1,rangeproof[1] = auction_p1.stage1_setup()
    pk_list_committee[2], encrypted_shares[2], LDEI_proof[2], tx2,rangeproof[2] = auction_p2.stage1_setup()
    pk_list_committee[3], encrypted_shares[3], LDEI_proof[3], tx3,rangeproof[3] = auction_p3.stage1_setup()
    # commitee setup verification
    LDEI_result = [None] * (n + 1)
    sig_committee = [None] * (n + 1)
    for i in range(1, n + 1):
        result = [None] * (n + 1)
        sig = [None] * (n + 1)
        result[1], sig[1] = committee_p1.setup_verification(tx1, pk_list_committee[i], n, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        result[2], sig[2] = committee_p2.setup_verification(tx1, pk_list_committee[i], n, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        result[3], sig[3] = committee_p3.setup_verification(tx1, pk_list_committee[i], n, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        assert result[1] and result[2] and result[3], "LDEI_proof is not true"
        LDEI_result[i] = result
        sig_committee[i] = sig
    # auction parties send setup to smart contract
    auction_p1.stage1_send_setup_to_smart_contract()
    auction_p2.stage1_send_setup_to_smart_contract()
    auction_p3.stage1_send_setup_to_smart_contract()
    # stage 1 broadcast
    x_upper_list = [None] * (max_len + 1)  # 二维数组
    xir_list_1, x_upper_list_1 = auction_p1.stage1_broadcast()
    xir_list_2, x_upper_list_2 = auction_p2.stage1_broadcast()
    xir_list_3, x_upper_list_3 = auction_p3.stage1_broadcast()
    for i in range(1, max_len + 1):
        xir_tuple_list = [None] * (n + 1)
        xir_tuple_list[1] = x_upper_list_1[i]
        xir_tuple_list[2] = x_upper_list_2[i]
        xir_tuple_list[3] = x_upper_list_3[i]
        x_upper_list[i] = xir_tuple_list
    # print("x_upper_list:", x_upper_list)

    # stage 1 compute_parameters_from_others
    # y_upper_list = [None] * (max_len + 1)  # 二维数组
    for i in range(1, max_len + 1):
        # print("x_upper_list[i][1:]", x_upper_list[i][1:])
        auction_p1.stage1_compute_parameters_from_others(i, x_upper_list[i][1:])
        auction_p2.stage1_compute_parameters_from_others(i, x_upper_list[i][1:])
        auction_p3.stage1_compute_parameters_from_others(i, x_upper_list[i][1:])
    #
    # stage 2 before first veto
    l_vir = [None] * (n + 1)
    l_rr = [None] * (n + 1)
    BV_proof_list = [None] * (n + 1)
    AV_proof_list = [None] * (n + 1)
    veto = [None] * (max_len + 1)
    last_veto_round = 0
    for i in range(1, max_len + 1):
        l_vir[1], l_rr[1], BV_proof_list[1] = auction_p1.stage2_before_first_veto(i)
        l_vir[2], l_rr[2], BV_proof_list[2] = auction_p2.stage2_before_first_veto(i)
        l_vir[3], l_rr[3], BV_proof_list[3] = auction_p3.stage2_before_first_veto(i)
        # stage 2 compute first veto and verify BV_proof
        veto[i], BV_result_1 = auction_p1.stage2_compute_before_first_veto(i, l_vir[1:], BV_proof_list[1:])
        veto[i], BV_result_2 = auction_p2.stage2_compute_before_first_veto(i, l_vir[1:], BV_proof_list[1:])
        veto[i], BV_result_3 = auction_p3.stage2_compute_before_first_veto(i, l_vir[1:], BV_proof_list[1:])

        # print("BV_result:", BV_result_1)
        assert BV_result_1, "BV proof is not true"
        if veto[i] == 1:
            last_veto_round = i
            break

    assert last_veto_round != 0, "All Veto is 0"

    before_first_veto_round = last_veto_round + 1

    for r in range(before_first_veto_round, max_len + 1):
        if r == 11: 
            print("round 11:")
        l_vir[1], l_rr[1], AV_proof_list[1] = auction_p1.stage2_after_first_veto(r, last_veto_round)
        l_vir[2], l_rr[2], AV_proof_list[2] = auction_p2.stage2_after_first_veto(r, last_veto_round)
        l_vir[3], l_rr[3], AV_proof_list[3] = auction_p3.stage2_after_first_veto(r, last_veto_round)

        veto[r], AV_result_1 = auction_p1.stage2_compute_after_first_veto(r, l_vir[1:], AV_proof_list[1:])
        veto[r], AV_result_2 = auction_p2.stage2_compute_after_first_veto(r, l_vir[1:], AV_proof_list[1:])
        veto[r], AV_result_3 = auction_p3.stage2_compute_after_first_veto(r, l_vir[1:], AV_proof_list[1:])

        assert AV_result_2, "AV proof is not true"

        if veto[r] == 1:
            last_veto_round = r
    winner_bid = utils.bit_array_to_int(veto[1:])
    print("winner price is: ", winner_bid)
    # stage 2 after first veto
    auction_p1.stage4_open_commitment(winner_bid)
    auction_p2.stage4_open_commitment(winner_bid)
    auction_p3.stage4_open_commitment(winner_bid)

    # result = contract.call_get_winner_info()
    # print(result)
