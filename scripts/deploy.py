from brownie import fundme, network, accounts, config, MockV3Aggregator
from scripts.helperfunctions import getaccount, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENT


def deploy_fundme():
    account = getaccount()

    # if we are on rinkeby, use associated address
    # 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
    # else use mock
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active(
        )]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fundme_contract = fundme.deploy(price_feed_address, {
                                    "from": account}, publish_source=config["networks"][network.show_active()].get("verify"))
    print("Contract deployed at {}", fundme_contract.address)
    return fundme_contract


def main():
    deploy_fundme()
