// SPDX-License-Identifier: MIT 
// SPDX-Licence-Identifier: GPL-3.0
pragma solidity ^0.8.19;

import "/Users/Patryk/.brownie/packages/smartcontractkit/chainlink-brownie-contracts@0.2.2/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
  
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed){
      priceFeed = AggregatorV3Interface(_priceFeed);
      owner = msg.sender;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUSD
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        // return (minimumUSD * precision) / price;
        // We fixed a rounding error found in the video by adding one!
        return ((minimumUSD * precision) / price) + 1;
    }

    modifier checkOwner(){
      require(msg.sender == owner, "you can not withdraw the founds!!!");
      _;
    }

    function withdraw() public payable checkOwner {
      payable(owner).transfer(address(this).balance);
      for (uint256 i=0;i<funders.length; i++){
          address funder = funders[i];
          addressToAmountFunded[funder] = 0;
      }
      funders = new address[](0);
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH!"
        );
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
      return priceFeed.version();
    }

    function getPrice() public view returns(uint256){
      (,int256 answer,,,
      ) = priceFeed.latestRoundData();
      return uint256(answer*10000000000);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }
}

