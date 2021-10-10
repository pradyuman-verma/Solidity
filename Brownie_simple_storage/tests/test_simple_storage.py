from brownie import SimpleStorage, accounts

# first test will be to check that our num initial value is equal to zero
def test_deploy():
    # Arrange - get an address
    account = accounts[0]
    # Act - deploy a contract
    simple_storage = SimpleStorage.deploy({"from": account})
    start_value = simple_storage.retrive()
    expected_value = 0
    # Assert
    assert start_value == expected_value


# testing updating feature
def test_update_value():
    # Arrange - get an address
    account = accounts[0]
    # Act - deploy a contract
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(15, {"from": account})
    updated_value = simple_storage.retrive()
    expected_value = 15
    # Assert
    assert updated_value == expected_value
