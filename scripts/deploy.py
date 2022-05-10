from brownie import accounts, config, chain, FidelToken, FidelTestBank, FidelTestBankV2
import time


                                        ##########################################
                                        #               Functions                #   
                                        ##########################################

#Deployment of the token and staking contracts
def deploy(fidel_account):
 
    #Deploy fidel token contract with a max supply of 100000
    fidel_token_contrat = FidelToken.deploy(100000,{"from": fidel_account})

    #Deploy the FidelTestBank contract
    fidelTestBank_contract = FidelTestBank.deploy(fidel_token_contrat, {"from": fidel_account})

    return fidel_token_contrat, fidelTestBank_contract

#Fund the FidelTestBank contract
def fundFidelTestBank(fidel_token_contrat, fidelTestBank_contract, fidel_account, fund_amount):

    #Funds the FidelTestBank contract
    fidel_token_contrat.stakeRewardPool(fund_amount, fidelTestBank_contract, {"from":fidel_account })


#Fidel funds the stakers(simple way to simulate that the stakers bought Fidel tokens from somewhere)
def fundStaker(dec_fit, fidel_token_contrat, fidel_account, staker_account, amount ):

    #Fund a staker
    fidel_token_contrat.transfer(staker_account, amount*dec_fit, {"from": fidel_account}) #funds the staker account amount x of tokens


#Stake   
def stake(dec_fit,fidel_token_contrat, fidelTestBank_contract, staker_account, stake_amount):

    #Stakers have to approve before transfering FidelTokens into the TestBank contract
    fidel_token_contrat.approve(fidelTestBank_contract,30*dec_fit, {"from": staker_account})

    #Staker1 stakes "stake_amount" nº of tokens
    fidelTestBank_contract.stakeTokens(stake_amount*dec_fit, {"from": staker_account})


#Retrieving gains after x hours and y minutes
def getRewards(dec_fit, fidel_token_contrat, fidelTestBank_contract, staker_account, hours_staked, minutes_staked):

    #Simulating the passing of nº hours and nº minutes (uneven division testing)
    chain.sleep(3600*hours_staked+60*minutes_staked)

    #Gets the rewards
    fidelTestBank_contract.getRewards({"from": staker_account})

    return fidel_token_contrat.balanceOf(staker_account)/(dec_fit)
    

#Unstake
def unstake(dec_fit, fidel_token_contrat, fidelTestBank_contract, staker_account):
    #We could just call the getRewards here if we wanted to do it automatically upon unstaking, 
    #as was described in the smart contracts comments 

    #Unstakes the tokens
    fidelTestBank_contract.unstakeTokens({"from": staker_account})

    return fidel_token_contrat.balanceOf(staker_account)/(dec_fit)


#Allow a user to migrate to a new contract
def migrateToNewContract(fidelTestBank_contract, fidelTestBankV2_contract, staker_account):

    #Fetchs the migrators balance
    balance = fidelTestBank_contract.stakingBalance(staker_account ,{"from": staker_account})
    #Fetchs the migrators time of staking
    time = fidelTestBank_contract.stakingTime(staker_account ,{"from": staker_account})

    #Staker asks to migrate
    fidelTestBank_contract.migrateToNewContract(fidelTestBankV2_contract ,{"from": staker_account})

    #Owner allows migration
    fidelTestBankV2_contract.allowMigration(staker_account, balance,time)

  


