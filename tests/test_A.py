from brownie import accounts, config, chain, FidelToken, FidelTestBank, FidelTestBankV2
import scripts.deploy as deployer

#Test description:
    #Deploy both the token and testbank contracts;
    #Fund the testbank contract with 100 tokens, in order to pay out the staking rewards to stakes
    #We fund a staker with 30 tokens
    #Make staker stake 2 tokens
    #Simulate the passage of 2hours and 3 minutes (account for uneven time division)
    #Make staker withdraw his rewards
    #Make staker unstake

def testA():
    #Decimal fit (standard 18 decimals in this case)
    dec_fit = 10**18

    #Define company account
    fidel_account = accounts[0] 

    #Get the contracts
    (fidel_token_contrat,fidelTestBank_contract)=deployer.deploy(fidel_account)

    #Fund the TestBank account with 100 tokens in order to be able to pay out the rewards to stakers
    deployer.fundFidelTestBank(fidel_token_contrat, fidelTestBank_contract, fidel_account, 100)

    #Define staker accoun
    staker1 = accounts[1] #

    #Fund staker account
    deployer.fundStaker(dec_fit, fidel_token_contrat, fidel_account, staker1, 30 )

    #Stake 2 tokens in the TestBank
    deployer.stake(dec_fit, fidel_token_contrat, fidelTestBank_contract, staker1, 2)#staker balance = 30 - 2 staked tokens = 28.0

#Results:
    expected1=28.0004
    assert expected1 == deployer.getRewards(dec_fit, fidel_token_contrat, 
                        fidelTestBank_contract, staker1, 2, 3)#gets 2hours*[0.001% of 2 staked tokens=0.0004] = 28.0004

    expected2 = 30.0004
    assert expected2 == deployer.unstake(dec_fit, fidel_token_contrat, fidelTestBank_contract,
                        staker1)#gets 28.0004+ [the initially 2 staked tokens] = 30.0004