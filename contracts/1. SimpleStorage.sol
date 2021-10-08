// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract SimpleStorage {
    uint num;
    
    struct People {
        uint num;
        string name;
    }
    
    People[] public arr;
    mapping (string => uint) hashmap;
    function store(uint256 _num) public {
        num = _num;
    }
    
    function retrive() public view returns (uint256){
        return num;
    }
    
    function addPerson(uint _num, string memory _name) public {
        arr.push(People(_num, _name));
        hashmap[_name] = _num;
    }
}