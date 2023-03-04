from web3 import Web3
import os
import time
from bytecodes import deployerByteCode, marketByteCode, zinkcoinbytecode, controllerByteCode

w3 = Web3(Web3.HTTPProvider("https://polygon-mumbai.infura.io/v3/8e0e615d913549cab4693265bc1725d7"))
assert w3.isConnected(), "Not connected to Ethereum node"
admin01 = w3.eth.account.from_key("92a8b880d49faa02af6156e35f6462cbc40a8e8094e88550d1c50effb833422f")
print(admin01.address)

# trans_json = {'chainId': w3.eth.chain_id,
#      'gas': 8 * 10 ** 6,
#      'gasPrice': w3.eth.gas_price,
#      'value': 0,
#      'from': admin01.address,
#      'nonce': w3.eth.get_transaction_count(admin01.address),
#      'to': None,
#      'data': deployerByteCode}

# signed_txn = w3.eth.account.signTransaction(trans_json, admin01.key)
# txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
# print("deployer hash:", txn_hash.hex())
# 0x1430094C57E348a39dc477fFf723Dd478016edBc

# time.sleep(20)
# txn_rcp = w3.eth._get_transaction_receipt(txn_hash.hex())
# print(txn_rcp)
# deployerAddress = txn_rcp['contractAddress']
# print("deployer address:", deployerAddress)
# 0x145ef42156fb27b75b3118E69D2Ed30ccD82BE85

#####################################################
# deploy zinkcoin
#####################################################

# trans_json = {'chainId': w3.eth.chain_id,
#      'gas': 5 * 10 ** 6,
#      'gasPrice': w3.eth.gas_price,
#      'value': 0,
#      'from': admin01.address,
#      'nonce': w3.eth.get_transaction_count(admin01.address),
#      'to': None,
#      'data': "0x"+zinkcoinbytecode}

# signed_txn = w3.eth.account.signTransaction(trans_json, admin01.key)
# txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
# print("zinkcoin tx hash:", txn_hash.hex())
# time.sleep(20)
# txn_rcp = w3.eth._get_transaction_receipt(txn_hash.hex())
# print(txn_rcp)
# zinkcoinAddress = txn_rcp['contractAddress']
# print("zinkcoin address:", zinkcoinAddress)
# zinkcoin address: 0x8a4470b6adDFc76E787437fD60060C31866AE5e1


#############################################################
# deploy controllerByteCode
############################################################
trans_json = {'chainId': w3.eth.chain_id,
     'gas': 8 * 10 ** 6,
     'gasPrice': w3.eth.gas_price,
     'value': 0,
     'from': admin01.address,
     'nonce': w3.eth.get_transaction_count(admin01.address),
     'to': None,
     'data': controllerByteCode}

signed_txn = w3.eth.account.signTransaction(trans_json, admin01.key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print("market tx hash:", txn_hash.hex())
time.sleep(20)
txn_rcp = w3.eth._get_transaction_receipt(txn_hash.hex())
print(txn_rcp)
cAddress = txn_rcp['contractAddress']
print("controllerByteCode address:", cAddress)
# 0x3Ea5beB64dE2dd48d2f9884dAA905235a0E5E0db



