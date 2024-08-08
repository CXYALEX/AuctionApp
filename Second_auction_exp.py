import random

from AuctionParty import AuctionParty
from CommitteeParty import CommitteeParty
from Interaction_SC.AuctionSC import AuctionSC
from utils import utils
from utils.utils_crpto import UtilsCrpto
import timeit

BIT_LEN = 256

def experiment():
    print("Auction Begin:")
    # prepare paremeters
    n = 4 #number of the auction parties
    max_len = 16 #length of the bid
    n_commitee = 3
    
    # read paremeters from smartcontract
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
    
    # auction_p1 = AuctionParty(1, 5 + pow(2, 31), max_len, 3)
    auction_p = [None] * (n + 1)

    for i in range(1,n+1):
        bid = random.randint(1, pow(2,max_len) -1)
        print("BID",i,":",bid)
        auction_p[i] = AuctionParty(i, bid, max_len, n)

    # auction_p[1] = AuctionParty(1, 26271, max_len, 3)
    # auction_p[2] = AuctionParty(2, 26272, max_len, 3)
    # auction_p[3] = AuctionParty(3, 26273, max_len, 3)
    # auction parties stage1 sutup
    encrypted_shares = [None] * (n + 1)
    LDEI_proof = [None] * (n + 1)
    pk_list_committee = [None] * (n + 1)
    rangeproof = [None] * (n + 1)

    for t in range(1,n+1):
        pk_list_committee[t], encrypted_shares[t], LDEI_proof[t], tx1,rangeproof[t] = auction_p[t].stage1_setup()
    
    # commitee setup verification
    LDEI_result = [None] * (n + 1)
    sig_committee = [None] * (n + 1)
    for i in range(1, n + 1):
        result = [None] * (n + 1)
        sig = [None] * (n + 1)
        result[1], sig[1] = committee_p1.setup_verification(tx1, pk_list_committee[i], n_commitee, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        result[2], sig[2] = committee_p2.setup_verification(tx1, pk_list_committee[i],  n_commitee, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        result[3], sig[3] = committee_p3.setup_verification(tx1, pk_list_committee[i], n_commitee, encrypted_shares[i],
                                                            LDEI_proof[i],rangeproof[i])
        assert result[1] and result[2] and result[3], "LDEI_proof is not true"
        LDEI_result[i] = result
        sig_committee[i] = sig
    # auction parties send setup to smart contract
    auction_p[1].stage1_send_setup_to_smart_contract()
    auction_p[2].stage1_send_setup_to_smart_contract()
    auction_p[1].stage1_send_setup_to_smart_contract()
    # stage 1 broadcast
    x_upper_list = [None] * (max_len + 1)  # 二维数组
    x_upper = [None] * (n + 1)  # 二维数组
    for t in range(1,n+1):
        _, x_upper[t] = auction_p[t].stage1_broadcast()
        # xir_list_2, x_upper_list_2 = auction_p[2].stage1_broadcast()
        # xir_list_3, x_upper_list_3 = auction_p[3].stage1_broadcast()
    for i in range(1, max_len + 1):
        xir_tuple_list = [None] * (n + 1)
        # xir_tuple_list[1] = x_upper_list_1[i]
        # xir_tuple_list[2] = x_upper_list_2[i]
        # xir_tuple_list[3] = x_upper_list_3[i]
        # x_upper_list[i] = xir_tuple_list
        for t in range(1,n+1):
            xir_tuple_list[t] = x_upper[t][i]
        x_upper_list[i] = xir_tuple_list
    # print("x_upper_list:", x_upper_list)

    # stage 1 compute_parameters_from_others
    # y_upper_list = [None] * (max_len + 1)  # 二维数组
    for i in range(1, max_len + 1):
        # print("x_upper_list[i][1:]", x_upper_list[i][1:])
        for t in range(1,n+1):
            auction_p[t].stage1_compute_parameters_from_others(i, x_upper_list[i][1:])

    #
    # stage 2 before first veto
    l_vir = [None] * (n + 1)
    l_rr = [None] * (n + 1)
    BV_proof_list = [None] * (n + 1)
    AV_proof_list = [None] * (n + 1)
    veto = [None] * (max_len + 1)
    last_veto_round = 0
    
    winnerpid = 0

    for i in range(1, max_len + 1):
        for t in range(1,n+1):
            l_vir[t], l_rr[t], BV_proof_list[t] = auction_p[t].stage2_before_first_veto(i)
        
        # stage 2 compute first veto and verify BV_proof
        for t in range(1,n+1):
            veto[i], BV_result, winnerpid = auction_p[t].spa_stage2_compute_before_first_veto(i, l_vir[1:], BV_proof_list[1:])
            assert BV_result, "BV proof is not true"
            # if find the only winner, move to the stage 3b
            if winnerpid !=0:
                print("i am the only winner, my pid is: ", winnerpid)
                break
        
        if veto[i] == 1:
            last_veto_round = i
            break

    assert last_veto_round != 0, "All Veto is 0"

    before_first_veto_round = last_veto_round + 1
    
    for r in range(before_first_veto_round, max_len + 1):
        if winnerpid !=0:
            break
        for i in range(1,n+1):
            l_vir[i], l_rr[i], AV_proof_list[i] = auction_p[i].stage2_after_first_veto(r, last_veto_round)


        for i in range(1,n+1):
            veto[r], AV_result, winnerpid = auction_p[i].spa_stage2_compute_after_first_veto(r, l_vir[1:], AV_proof_list[1:])
            assert AV_result, "AV proof is not true"
            # if find the only winner, move to the stage 3b
            if winnerpid !=0:
                print("i am the only winner, my pid is: ", winnerpid)
                break


        if veto[r] == 1:
            last_veto_round = r

    print("the winner is: ", winnerpid)
    
    # winner_bid = utils.bit_array_to_int(veto[1:])
    # print("winner price is: ", winner_bid)
    # # stage 2 after first veto
    # auction_p[1].stage4_open_commitment(winner_bid)
    # auction_p[2].stage4_open_commitment(winner_bid)
    # auction_p[3].stage4_open_commitment(winner_bid)

    # result = contract.call_get_winner_info()
    # print(result)

    # stage3b
    for i in range(1, max_len + 1):
        # print("x_upper_list[i][1:]", x_upper_list[i][1:])
        for t in range(1,n+1):
            if t == winnerpid:
                continue
            auction_p[t].stage3b_recompute_parameters_from_others_exclude_w(i, x_upper_list[i][1:], winnerpid)

    
     # stage 2 before first veto
    l_vir = [None] * (n + 1)
    l_rr = [None] * (n + 1)
    BV_proof_list = [None] * (n + 1)
    AV_proof_list = [None] * (n + 1)
    veto = [None] * (max_len + 1)
    last_veto_round = 0
    

    for i in range(1, max_len + 1):
        for t in range(1,n+1):
            if t == winnerpid:
                continue
            l_vir[t], l_rr[t], BV_proof_list[t] = auction_p[t].stage2_before_first_veto(i)
        
        # stage 2 compute first veto and verify BV_proof
        for t in range(1,n+1):
            if t == winnerpid: 
                continue
            veto[i], BV_result= auction_p[t].stage3b_compute_before_first_veto_exclude_w(i, l_vir[1:], BV_proof_list[1:])
            assert BV_result, "BV proof is not true"
        
        if veto[i] == 1:
            last_veto_round = i
            break

    assert last_veto_round != 0, "All Veto is 0"

    before_first_veto_round = last_veto_round + 1
    
    for r in range(before_first_veto_round, max_len + 1):
        for i in range(1,n+1):
            if i == winnerpid:
                continue
            l_vir[i], l_rr[i], AV_proof_list[i] = auction_p[i].stage2_after_first_veto(r, last_veto_round)


        for i in range(1,n+1):
            if i == winnerpid:
                continue
            veto[r], AV_result = auction_p[i].stage3b_compute_after_first_veto_exclude_w(r, l_vir[1:], AV_proof_list[1:])
            assert AV_result, "AV proof is not true"


        if veto[r] == 1:
            last_veto_round = r

    winner_bid = utils.bit_array_to_int(veto[1:])
    print("the second price is: ", winner_bid)

    for i in range(1,n+1):
        auction_p[i].stage4_open_commitment(winner_bid)
    result = contract.call_get_winner_info()

if __name__ == "__main__":
    # 使用 timeit 测量单次执行时间
    execution_time = timeit.timeit("experiment()", setup="from __main__ import experiment", number=100)
    average_time = execution_time / 100
    print(f"Average execution time over 100 runs: {average_time:.4f} seconds") 