import json
import os

from web3 import Web3
from solcx import compile_standard, install_solc
from dotenv import load_dotenv

# this funtcion will look for .env file and automatically imports it to our script
load_dotenv()

print("Reading file ...")
with open("../contracts/1. SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# print(simple_storage_file)

# installing solidity compiler
# print("Installing...")
install_solc("0.6.0")

# compiling the solidity code.
print("Compiling ...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "../contracts/1. SimpleStorage.sol": {"content": simple_storage_file}
        },
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)
# dumping our compiled_sol as a json file
with open("compliled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Soon we will depoly our solidity contract, to do so we need our cod bytecode.
bytecode = compiled_sol["contracts"]["../contracts/1. SimpleStorage.sol"][
    "SimpleStorage"
]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["../contracts/1. SimpleStorage.sol"]["SimpleStorage"][
    "abi"
]

# print(abi, bytecode)

# connecting to ganache
print("Connecting to web3 provider...")
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x50a6fd6B1bB4bD3640a06536D09A8eCd7F01fAD1"
# private_key = "0xc30c91053aa907ed4002018e44a7670f9d28eda5a2575b444972c5370843e699"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# 1. build a transaction
# 2. Sign a transaction
# 3. send a transaction
# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# building a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# signing the transaction
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
# print(private_key)

# sending this transaction
print("Deploying Contact..")
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# waiting for transaction confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Yay! Contract Succesfully deployed")

# Wokring with contract - we need two thing to work with contract which is on chain
# 1. Contract Adress
# 2. Contract ABI

# creating contract object to work with it.
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# now we can interact with it as we do in remix
# Two ways we can interact with a contract.
# call -> Simulate making the call and getting a return value (similar to blue buttons on remix)
# transact -> Actually make a state change

# printing initial value of num
# print(simple_storage.functions.retrive().call())
# updating value temporary using call
# print(simple_storage.functions.store(18).call())

# updating value permanently
print("Updating Contract ...")
store_tx = simple_storage.functions.store(18).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_tx = w3.eth.account.sign_transaction(store_tx, private_key)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("Yay! Contract updated Succesfully")
print(simple_storage.functions.retrive().call())
