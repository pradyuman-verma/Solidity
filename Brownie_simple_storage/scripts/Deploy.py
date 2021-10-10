# brownie makes life easy, thats why we use it
# it automatically compiles code.
# it automatically dumps json to a file in build/contracts
# it also gives us abi and bytecode.
# it aumatically launches local blockchain - ganache-cli

# to get address and private, brownie has a accounts package to help with that
from brownie import accounts, config, SimpleStorage
import os


def deploy_simple_storage():
    # 1. As ganache-cli spins up 10 accounts to us.
    # only works for ganache-cli
    account = accounts[0]

    # 2. For manually added account - it will ask for password in cli (most secure way)
    # account = accounts.load("Prady001")

    # 3. using envirnment variable
    # account = accounts.add(os.getenv("PRIVATE_KEY"))

    # 3b. making it more secure
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    # deploying the contract - returns contract object
    simple_storage = SimpleStorage.deploy({"from": account})
    # print(simple_storage)
    stored_value = simple_storage.retrive()
    # brownie is smart enough is to know whether we want to use call or transact
    print(stored_value)
    # updating the initial value
    transaction = simple_storage.store(18, {"from": account})
    # waiting for one block confirmation
    transaction.wait(1)
    updated_value = simple_storage.retrive()
    print(updated_value)


def main():
    deploy_simple_storage()
