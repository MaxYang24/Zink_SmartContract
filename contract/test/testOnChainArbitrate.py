from web3 import Web3
import os
import time
from eth_account.messages import encode_defunct
import binascii


w3 = Web3(Web3.HTTPProvider(
    "https://polygon-mumbai.g.alchemy.com/v2/-dSjCpSmQAIk3nwZ45vNsBxg1DMydqK5/"))
assert w3.isConnected(), "Not connected to Ethereum node"
ZINKCoinAddress = "0xafc26ad91a100b3e012a0f6cfebe34aaf2424c9b"
ZINKAllinoneAddress = "0x9a9dde43fef2fa8e739289433e0ae0155d1adcfa"
ZINKCoin = w3.eth.contract(address=w3.toChecksumAddress(ZINKCoinAddress), abi=open(
    os.path.dirname(os.path.abspath(__file__)) + "/ZINKCoin.json", "r").read())
ZINKAllinone = w3.eth.contract(address=w3.toChecksumAddress(ZINKAllinoneAddress), abi=open(
    os.path.dirname(os.path.abspath(__file__)) + "/ZINKAllinone.json", "r").read())
admin01 = w3.eth.account.from_key(
    "92a8b880d49faa02af6156e35f6462cbc40a8e8094e88550d1c50effb833422f")
st01 = w3.eth.account.from_key(
    "c0699a6be538361b02edc43a2918863fb5a961ac3a3b34eae7d9d990c7c05ed2")
print("student addr:", st01.address)
tc01 = w3.eth.account.from_key(
    "29209a5b8e9a331ed0c7aca5e33ba7011feb81e495f48b5cfa4a95d365ff542f")
print("teacher addr:", tc01.address)


# prepare order
prepareOrderTxRaw = ZINKAllinone.functions.prepareOrder([1, st01.address, "https://www.google.com", "https://www.google.com", "0x1111111111111111111111111111111111111111111111111111111111111111", 0, 0, 1000, tc01.address, 12345678, 0]).buildTransaction(
    {
        'chainId': w3.eth.chain_id,
        'gas': 5 * 10 ** 6,
        'gasPrice': w3.eth.gas_price,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(admin01.address),
        'from': admin01.address
    }
)
signedPrepareOrderTx = w3.eth.account.signTransaction(
    prepareOrderTxRaw, admin01.key)
signedPrepareOrderTxhash = w3.eth.sendRawTransaction(
    signedPrepareOrderTx.rawTransaction)
print("prepare order:", signedPrepareOrderTxhash.hex())
time.sleep(10)


# get last tx
lastOrderId = ZINKAllinone.functions.orderNum().call() - 1
print("last Order Id is ", lastOrderId)

# get Order Hash
OrderHash = ZINKAllinone.functions.genCreatOrderHash(lastOrderId).call()
print(OrderHash.hex())

# student sig
message = encode_defunct(hexstr=OrderHash.hex())
st01signature = w3.eth.account.sign_message(message, st01.privateKey)
st01sig = st01signature.signature.hex()

# teacher sig
message = encode_defunct(hexstr=OrderHash.hex())
tc01signature = w3.eth.account.sign_message(message, tc01.privateKey)
tc01sig = tc01signature.signature.hex()


delegateCreateOrderTxRaw = ZINKAllinone.functions.ZINKAdminDelegateCreateOrder(lastOrderId, binascii.unhexlify(st01sig[2:]), binascii.unhexlify(tc01sig[2:])).buildTransaction(
    {
        'chainId': w3.eth.chain_id,
        'gas': 5 * 10 ** 6,
        'gasPrice': w3.eth.gas_price,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(admin01.address),
        'from': admin01.address
    }
)

delegateCreateOrderTx = w3.eth.account.signTransaction(
    delegateCreateOrderTxRaw, admin01.key)
delegateCreateOrderTxhash = w3.eth.sendRawTransaction(
    delegateCreateOrderTx.rawTransaction)
print("create order hash:", delegateCreateOrderTxhash.hex())
time.sleep(10)
#########################
#
DelegateArbitrateOrderRawTx = ZINKAllinone.functions.ZINKAdminDelegateApplyArbitratingOrder(lastOrderId).buildTransaction(
    {
        'chainId': w3.eth.chain_id,
        'gas': 5 * 10 ** 6,
        'gasPrice': w3.eth.gas_price,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(admin01.address),
        'from': admin01.address
    }
)
DelegateArbitrateOrder = w3.eth.account.signTransaction(
    DelegateArbitrateOrderRawTx, admin01.key)
DelegateArbitrateOrderTxhash = w3.eth.sendRawTransaction(
    DelegateArbitrateOrder.rawTransaction)
print("arbitrateOrder:", DelegateArbitrateOrderTxhash.hex())
time.sleep(10)
##################################################
# apply arbitrate
pOne = w3.eth.account.create()
print("pOne addr:", pOne.address)
pTwo = w3.eth.account.create()
print("pTwo addr:", pTwo.address)
pThree = w3.eth.account.create()
print("pThree addr:", pThree.address)

supportHash = ZINKAllinone.functions.genArbitrateHash(1, lastOrderId).call()
oneM = encode_defunct(hexstr=supportHash.hex())
twoM = encode_defunct(hexstr=supportHash.hex())
threeM = encode_defunct(hexstr=supportHash.hex())

v01signature = w3.eth.account.sign_message(oneM, pOne.privateKey)
v02signature = w3.eth.account.sign_message(twoM, pTwo.privateKey)
v03signature = w3.eth.account.sign_message(threeM, pThree.privateKey)

v01sig = v01signature.signature.hex()
print("v01 sig:", v01sig)
v02sig = v02signature.signature.hex()
print("v02 sig:", v02sig)
v03sig = v03signature.signature.hex()
print("v03 sig:", v03sig)

sfarTxRaw = ZINKAllinone.functions.ZINKAdminDelegateSubmitFinalArbitrationResult(lastOrderId, [1, 1, 1, pOne.address, pTwo.address, pThree.address, binascii.unhexlify(v01sig[2:]), binascii.unhexlify(v02sig[2:]), binascii.unhexlify(v03sig[2:])]).buildTransaction(
    {
        'chainId': w3.eth.chain_id,
        'gas': 5 * 10 ** 6,
        'gasPrice': w3.eth.gas_price,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(admin01.address),
        'from': admin01.address
    }
)
sfarTxSigned = w3.eth.account.signTransaction(sfarTxRaw, admin01.key)
sfarTxSignedHash = w3.eth.sendRawTransaction(sfarTxSigned.rawTransaction)
print("sfar hash:", sfarTxSignedHash.hex())
