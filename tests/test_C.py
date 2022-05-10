from brownie import accounts, config, chain, FidelToken, FidelTestBank, FidelTestBankV2
import scripts.deploy as deployer

#Test description:
    #Deploy both the token and testbank contracts;
    #Fund the testbank contract with 100 tokens, in order to pay out the staking rewards to stakes
    #We fund a staker with 30 tokens
    #Make staker stake 2 tokens
    #Simulate the passage of 1 hour and 3 minutes (account for uneven time division)
    #Make staker upgrade to a new contract
    #Simulate the passage of 2 hours
    #Make staker claim rewards
 
 
def testC():
    #Decimal fit (standard 18 decimals in this case)
    dec_fit = 10**18

    #Define company account
    fidel_account = accounts[0] 

    #Get the contracts
    (fidel_token_contrat,fidelTestBank_contract)=deployer.deploy(fidel_account)

    #Fund the TestBank account with 100 tokens in order to be able to pay out the rewards to stakers
    deployer.fundFidelTestBank(fidel_token_contrat, fidelTestBank_contract, fidel_account, 100)

    #Define staker account
    staker1 = accounts[1] #

    #Fund staker account
    deployer.fundStaker(dec_fit, fidel_token_contrat, fidel_account, staker1, 30 )

    #Stake 2 tokens in the TestBank
    deployer.stake(dec_fit, fidel_token_contrat, fidelTestBank_contract, 
                   staker1, 2)#staker balance = 30 - 2 staked tokens = 28.0
    
    #Simulate the passge of 1 hour and 3 minutes.
    chain.sleep(3600*1+60*3)# Staker balance = 28, Rewards = 0.0002

    #Deploy new/upgraded contract
    fidelTestBankV2_contract = FidelTestBankV2.deploy(fidel_token_contrat, {"from": fidel_account})

    #Fund the new contract with 100 Fidel Tokens
    deployer.fundFidelTestBank(fidel_token_contrat, fidelTestBankV2_contract, fidel_account, 100)

    #Migrate the staker to the new contract
    deployer.migrateToNewContract(fidelTestBank_contract, fidelTestBankV2_contract, 
                                  staker1)#Status in new contract: staker balance = 28, Rewards = 0.0002

#Results:
    expected1=28.0006
    assert expected1 == deployer.getRewards(dec_fit, fidel_token_contrat, fidelTestBankV2_contract, 
                        staker1, 2, 0)#2 horus pass and the user withdraws the rewards
                                      #Rewards 0.0002 [old contract time]+0.0004[new...time]=0.0006
                                      #Balance = 28.0006
