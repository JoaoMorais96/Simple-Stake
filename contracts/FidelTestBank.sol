// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.4.2/contracts/access/Ownable.sol";

contract FidelTestBank is Ownable{

    IERC20 public FIDELTEST;//Fidel Token contract interface

    //Staker address => amount staked
    mapping(address => uint256) public stakingBalance;

    //Staker address => when he staked
    mapping(address => uint256) public stakingTime;

    constructor(address _FIDELTESTAddress) {
        FIDELTEST = IERC20(_FIDELTESTAddress);
    }

    // Stake token
        //Simple way to stake in this contract and keep track of it.
        //I decided to make it so the staker can only stake once at a time.
        //This is because the code would have to keep a struct of every deposit amount and time of creation,
        //make a mapping of address=>deposits[]
        //and then calculate the calcRewards() for each individual staker.
        //Although this is not that hard, it would make the testing pretty calculation-heavy to ensure
        //the rewards are correct, so I think it's better to do it this way for this simple exercise.
    function stakeTokens(uint256 _amount) public {
        // Require amount greater than 0
        require(_amount > 0, "amount cannot be 0");

        //Require that the staker hasn't already staked a certain amount
        require(stakingBalance[msg.sender]==0, "You have already staked.");

        //Transfer tokens from the staker to this contract
        FIDELTEST.transferFrom(msg.sender, address(this), _amount);

        //Update the mapping to save the stakers balance
        stakingBalance[msg.sender] = _amount;

        //Update the mapping to save the stakers balance  
        stakingTime[msg.sender]=block.timestamp;
    }

    // Unstaking Tokens (Withdraw)
        //I required the user to withdraw the awards first before he can unstake.
        //This is done to avoid having to run getRewards() at the time of unstaking, which
        //Saves gas if the staker currently has no rewards (aka has staked or withdrawn the 
        //rewards less than an hour ago).
        //Regardless, this could easilly be done in the backend if we wanted(see the comments in deploy.py)
    function unstakeTokens() public {
        // Fetch staking balance
        uint256 balance = stakingBalance[msg.sender];
        // Fetch reward balance
        uint256 reward = calcRewards(msg.sender);

        // Require the suer to have some amount staked
        require(balance > 0, "Staking balance cannot be 0");
        // Require the user to have claimed his staking rewards
        require(reward == 0, "Please claim your rewards before unstaking.");

        //Update mapping
        stakingBalance[msg.sender] = 0;

        //Transfer tokens back to user
        FIDELTEST.transfer(msg.sender, balance);
    }

    // Withdraw the rewards
        //This could have been done in such a way that only the owner of the contract can distribute the rewards
        //for all stakers. Although this can work in a DEX enviornment, it's not really that decentralized.
        //It also wastes gas because some stakers won't have rewards yet, but we still do calculations.
        //So I opted for a user-centric approach, where each one can retrieve his awards,
    function getRewards() public {

        //Fetch the balance of this contract
        uint contractBalance = FIDELTEST.balanceOf(address(this));

        //Require that the contract has enough balance to pay out the awards
        require(FIDELTEST.balanceOf(address(this))>0, "No more tokens to reward.");
     
        // Require the user to have some amount staked
        require(stakingBalance[msg.sender] > 0, "Staking balance cannot be 0");

        //Fetch how much the staker is owed
        uint rewards = calcRewards(msg.sender);

        //Updates the mapping
        stakingTime[msg.sender]= block.timestamp;

        //If the contract doesn't have enough money to pay the reward
        //(this is not likely to happen, but it can happen by miscalculation)
        if(rewards>contractBalance){
            //Issue the full token amount to the requester
            FIDELTEST.transfer(msg.sender, contractBalance);
        }else{
            //Issue the full token amount to the requester
            FIDELTEST.transfer(msg.sender, rewards);
        }
    }

    // Calculate the rewards to give to the staker        
        //Can be done when the staker wants to withdraw his rewards. This way we save transactions
        //by only calculating this when it is requested/needed
    function calcRewards(address _recipient) internal returns(uint256){
        uint rewardPerHour = stakingBalance[_recipient]/10000;
        uint hoursPassed = (block.timestamp - stakingTime[_recipient])/3600;

        return rewardPerHour*hoursPassed;
    }

    // Migrate
        //The most used way to do this would be to use a proxy and just update the contract.
        //But that would mean that it is not actually a choice that the user can make,
        //he will just be transfered to the new contract without making a choice (which I understood is what is asked).
        //So I opted for a user-centric approach. The user only pays for the migrateToNewContract(),
        //while the contract creator pays for the "entering" of the info in the new contract.
        //I think this makes sense, seeing as it is the contract creators fault that there is an exploit
    function migrateToNewContract(address _newContract) public {

        //Require the migrator to have something staked
        require( stakingBalance[msg.sender]>0, "You are not staking anything.");

        //Update mappings
        stakingBalance[msg.sender]=0;
        stakingTime[msg.sender]=0;

        // Sends the staked tokens to the new contract
        FIDELTEST.transfer(_newContract, stakingBalance[msg.sender]);
    } 

    

}

