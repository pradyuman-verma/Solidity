// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./1. SimpleStorage.sol";

contract SimpleFactory is SimpleStorage {
    SimpleStorage[] public simpleArr;

    function createSimpleStorage() public {
        SimpleStorage simple = new SimpleStorage();
        simpleArr.push(simple);
    }

    function sfStore(uint256 _num, uint256 _idx) public {
        SimpleStorage(address(simpleArr[_idx])).store(_num);
    }

    function sfGet(uint256 _idx) public view returns (uint256) {
        return SimpleStorage(address(simpleArr[_idx])).retrive();
    }
}
