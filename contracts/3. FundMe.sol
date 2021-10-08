// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
    
    address public owner;
    address[] public funders;
    mapping (address => uint256) public fundingAddress;
    
    constructor() public{
        owner = msg.sender;
    }
    
    function fundMe() public payable {
        fundingAddress[msg.sender] = msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }
    
    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (, int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }
    
    function getConversionRate(uint ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 amtInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return amtInUsd;
    } 
    
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    
    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        
        for (uint i = 0; i < funders.length; i ++) {
            fundingAddress[funders[i]] = 0;
        }
        funders = new address[](0);
    }
}