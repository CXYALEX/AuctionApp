# Auction App

## 1. Description
This is the experience for the paper  [FAST: Fair Auctions via Secret Transactions](https://eprint.iacr.org/2021/264.pdfl)

## 2. Dependency
### 2.1 pybulletproofs
Use pyO3 to create a pybulletproofs library.
1. You are required to git clone the [pybulletproofs](https://github.com/initc3/pybulletproofs).
2. create the pyrust library for pybulletproofs
```sh
cargo new pybulletproofs --lib
```
3. build pybulletproofs project
```sh
Cargo build --release
```


## 3. Deploy the auction smart contract
Deploy the auction smart contract： https://github.com/CXYALEX/AuctionContract
1. build project
```sh
make build 
```
2. Start Anvil 
```sh
make anvil
```
3. deploy contract
```sh
make deploy
```


## 4. Run the second auction experience
```python
python3 Second_auction_exp.py
```

## 5. Experiment Result
Run the experience 100 times for 4 parties or 8 parties.
|       | 4 party| 8 party  |
|-------|---------|----------|
| **16**| 9.7806s | 11.1929s |