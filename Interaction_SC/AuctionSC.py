import json

from web3 import Web3, HTTPProvider

from utils.utils_crpto import UtilsCrpto


class AuctionSC:
    def __init__(self, anvil_rpc, contract_address, abi_file, private_key):
        self.anvil_rpc = anvil_rpc
        self.contract_address = contract_address
        self.private_key = private_key
        with open(abi_file, 'r') as f:
            self.abi = json.loads(f.read())['abi']
        self.web3 = Web3(HTTPProvider(anvil_rpc))
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def get_balance(self):
        balance = self.web3.from_wei(self.web3.eth.get_balance(self.contract_address), "ether")
        return balance

    def send_set_generator(self, g, h):
        assert isinstance(g, bytes), "g is not bytes"
        assert isinstance(g, bytes), "h is not bytes"
        account = self.web3.eth.account.from_key(self.private_key)
        account_address = account.address
        transaction = self.contract.functions.setGenerator(g, h).build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gas': 200000,
            # 'value': self.web3.to_wei('3', 'ether'),
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, account._private_key)
        send_store_tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_store_tx)
        print(tx_receipt)

    def send_set_prime(self, p, q):
        assert isinstance(p, bytes), "p is not bytes"
        assert isinstance(q, bytes), "q is not bytes"
        account = self.web3.eth.account.from_key(self.private_key)
        account_address = account.address
        transaction = self.contract.functions.setPrime(p, q).build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gas': 200000,
            # 'value': self.web3.to_wei('3', 'ether'),
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, account._private_key)
        send_store_tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_store_tx)
        print(tx_receipt)

    def send_set_pkcList(self, index, pk):
        assert isinstance(index, int), "index is not int"
        assert isinstance(pk, bytes), "pk is not bytes"
        account = self.web3.eth.account.from_key(self.private_key)
        account_address = account.address
        transaction = self.contract.functions.setpkcList(index, pk).build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gas': 200000,
            # 'value': self.web3.to_wei('3', 'ether'),
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, account._private_key)
        send_store_tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # timeout = 5 seconds
        try:
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_store_tx, timeout=5)
            print(tx_receipt)
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")

    def call_get_generator(self):
        try:
            result = self.contract.functions.getGenerator().call()
            return result
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")

    def send_setup(self, pid, id, value):
        account = self.web3.eth.account.from_key(self.private_key)
        account_address = account.address
        transaction = self.contract.functions.setup(pid, id, value).build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gas': 200000,
            # 'value': self.web3.to_wei('3', 'ether'),
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, account._private_key)
        send_store_tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # timeout = 5 seconds
        try:
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_store_tx, timeout=5)
            print(tx_receipt)
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")

    def send_openCommitment(self, pid, value, r):
        account = self.web3.eth.account.from_key(self.private_key)
        account_address = account.address
        transaction = self.contract.functions.openCommitment(pid, value, r).build_transaction({
            'nonce': self.web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gas': 200000,
            # 'value': self.web3.to_wei('3', 'ether'),
            'gasPrice': self.web3.to_wei('50', 'gwei')
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, account._private_key)
        send_store_tx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # timeout = 5 seconds
        try:
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_store_tx, timeout=5)
            print(tx_receipt)
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")

    def call_get_param(self):
        s_g, s_h, pkc_list = self.contract.functions.getParam().call()
        return s_g, s_h, pkc_list

    def call_get_prime(self):
        s_p, s_q = self.contract.functions.getPrime().call()
        return s_p, s_q

    def call_get_committee_count(self):
        s_commiteeCount = self.contract.functions.getCommiteeCount().call()
        print(s_commiteeCount)
        return (s_commiteeCount)

    def call_get_winner_info(self):
        try:
            result = self.contract.functions.getWinnerInfo().call()
            return result
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")

    def call_lhs(self):
        try:
            result = self.contract.functions.getlhs().call()
            return result
        except Web3.TimeExhausted as e:
            print(f"timeout:{e}")


if __name__ == '__main__':
    # 创建ContractBalance对象
    contract = AuctionSC('http://127.0.0.1:8545', '0x5FbDB2315678afecb367f032d93F642f64180aa3',
                         'Auction.json',
                         '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')

    # balance = contract.send_set_generator()
    p = 7703
    q = 3851
    g = 7698
    h = 7094
    contract.send_set_generator(UtilsCrpto.int_to_bytes(g), UtilsCrpto.int_to_bytes(h))
    contract.send_set_prime(UtilsCrpto.int_to_bytes(p), UtilsCrpto.int_to_bytes(q))
    pid = 1
    id = 1
    c = 5452
    contract.send_setup(pid, id, c)
    value = 42
    r = 10
    contract.send_openCommitment(pid, value, r)
    print(contract.call_get_winner_info())
    # 调用get_balance()方法获取余额
    # balance = contract.get_balance()
    # print(balance)
