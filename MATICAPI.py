# -------------------------------- LIBRARIES -------------------------------- #
from web3 import Web3
from web3.middleware import geth_poa_middleware
import Config as config
import time

# ------------------------------- MAIN CLASS -------------------------------- #
class MaticAPI(object):
# ------------------------------- INITIALIZE -------------------------------- #
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(config.MATIC_RPC_URL))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.start_balance = self.getBalance()
        self.contractWombat = self.web3.eth.contract(address=self.web3.toChecksumAddress(config.WOMBAT_CONTRACT_ADDRESS), abi=config.WPOO_ABI)

# ---------------------------------- UTILS ---------------------------------- #
    def getBalance(self):  # Get MATIC balance
        return self.web3.fromWei(self.web3.eth.get_balance(config.SENDER_ADDRESS), 'ether')

    def getNonce(self):  # Get address nonce
        return self.web3.eth.get_transaction_count(config.SENDER_ADDRESS)
        
# --------------------------------- WOMBAT --------------------------------- #
# --------------------------------- CLEAN --------------------------------- #
    def ownedWombats(self):
        sender = self.web3.toChecksumAddress(config.SENDER_ADDRESS)
        nonce = self.web3.eth.get_transaction_count(sender)
        
        ownedWombats = self.contractWombat.functions.ownedWombats(sender).call()
        
        return ownedWombats
        
    def cleanShit(self):
        sender = self.web3.toChecksumAddress(config.SENDER_ADDRESS)
        nonce = self.web3.eth.get_transaction_count(sender)
        
        ownedWombats = self.ownedWombats()
        wombatIDs = []
        for w in ownedWombats:
            wombatIDs.append(w[0])
                
        approve = self.contractWombat.functions.clean(wombatIDs).buildTransaction({
            'from': sender,
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.sign_transaction(approve, private_key=config.PRIVATE_KEY)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx = self.web3.toHex(tx_token)
        return tx
        