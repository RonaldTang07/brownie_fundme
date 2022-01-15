from brownie import network, accounts, config, MockV3Aggregator

DECIMALS = 8
STARTING_PRICE_IN_ETH = 200000000000

FORKED_BLOCKCHAIN_ENVIRONMENT = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]


def getaccount():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENT:
        account = accounts[0]
    else:
        account = accounts.add(config["wallets"]["from_key"])
    return account


def deploy_mocks():
    print("The active network is {}".format(network.show_active()))
    print("Deploying mock...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE_IN_ETH, {
                                "from": getaccount()})
