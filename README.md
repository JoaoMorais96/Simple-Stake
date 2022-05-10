# Summary
- An ERC20 token is created
- A contract is created that allows this token to be staked at a rate of 0.01% per hour passed
- The stking contract is upgradeable
# Prerequisites
Please install or have installed the following:

- nodejs and npm
- python

# Installation
1) Install Brownie, if you haven't already. Here is a simple way to install brownie.
   
> pip install eth-brownie

Or, if that doesn't work, via pipx

> pip install --user pipx
> 
> pipx ensurepath
> 
> #restart your terminal
> 
> pipx install eth-brownie

1) For local testing install ganache-cli
> npm install -g ganache-cli

or

> yarn add global ganache-cli

3) Download the mix and install dependancies.
> brownie bake upgrades-mix

> cd upgrades

# Test
All the tests are explained in comments on each test file in "./tests". 

Just run:
> brownie test


# Decisions
All the reasons for each decision are written in the code commentary (mostly on the FidelTestBank.sol), but here follows a summary:
1) Contract needs to be funded in order to distribute rewards: easy way to increase the amount to reward, if the Token owner wants to;
2) Unstaking can only be done after withdrawing gains: this is done to save some gas. However, this is easilly editable and has no importance overall so it could be changed on demand;
3) Rewards can only be withdrawn by the user instead of distributed by the contract owner: greater decentralization and also saves some gas;
4) Migration to new contract requires the staker to send money to the new contract and then the contract owner will update his info on the new contract: this is just a random way I thought of doing a migration that is entirely a users choice instead of a proxy, which is the contract owners choice