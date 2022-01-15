// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract fundme {
    mapping(address => uint256) public addresstoamountfunded;
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddress) {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function addfund() public payable {
        uint256 minimumUSD = 50 * 10**18;

        require(
            getconversionrate(msg.value) >= minimumUSD,
            "You need to deposite at least 50USD of ETH"
        );

        addresstoamountfunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getversion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getdecimals() public view returns (uint8) {
        return priceFeed.decimals();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getconversionrate(uint256 weiamount)
        public
        view
        returns (uint256)
    {
        uint256 currentprice = getPrice();
        return (currentprice * weiamount) / 1000000000000000000;
    }

    function getentrancefee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier owneronly() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public owneronly {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 index = 0; index < funders.length; index++) {
            addresstoamountfunded[funders[index]] = 0;
        }

        funders = new address[](0);
    }
}
