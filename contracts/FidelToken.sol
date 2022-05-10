// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/access/Ownable.sol";

contract FidelToken is ERC20, Ownable {
    constructor(uint _TotalSuply) ERC20("Fidel API Token", "FIDELTEST") {
        _mint(msg.sender, _TotalSuply* (10**18));
    }

    //Mints tokens directly into the FideTestBank contract to be distributed
    //Could also be done as a percentage of the existing tokens, but this way is easier if we
    //eventually decide that the token is inflationary
    function stakeRewardPool(uint _stakeRewardAmount, address _FidelTestBankAddress) public onlyOwner{
        _mint(_FidelTestBankAddress, _stakeRewardAmount*10**18);
    }
}
