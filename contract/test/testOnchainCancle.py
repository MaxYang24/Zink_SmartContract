from web3 import Web3
import os
import time
from eth_account.messages import encode_defunct
import binascii


w3 = Web3(Web3.HTTPProvider("https://cosmological-withered-wave.bsc-testnet.discover.quiknode.pro/8eb10320bb2923d1c5f7763dad488be0672d1c85/"))
assert w3.isConnected(), "Not connected to Ethereum node"
ZINKCoinAddress = "0xdeCFc22DABA063810546D0016C4a77C27F3E927E"
ZINKAllinoneAddress = "0x6F920A1bFA508b621bdA62C4C4b86D58D8421C3a"
ZINKCoin = w3.eth.contract(address=ZINKCoinAddress, abi=open(os.path.dirname(os.path.abspath(__file__)) + "/ZINKCoin.json", "r").read())
ZINKAllinone = w3.eth.contract(address=ZINKAllinoneAddress, abi=open(os.path.dirname(os.path.abspath(__file__)) + "/ZINKAllinone.json", "r").read())
admin01 = w3.eth.account.from_key("92a8b880d49faa02af6156e35f6462cbc40a8e8094e88550d1c50effb833422f")
st01 = w3.eth.account.from_key("c0699a6be538361b02edc43a2918863fb5a961ac3a3b34eae7d9d990c7c05ed2")
print("student addr:", st01.address)
tc01 = w3.eth.account.from_key("29209a5b8e9a331ed0c7aca5e33ba7011feb81e495f48b5cfa4a95d365ff542f")
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
signedPrepareOrderTx = w3.eth.account.signTransaction(prepareOrderTxRaw, admin01.key)
signedPrepareOrderTxhash = w3.eth.sendRawTransaction(signedPrepareOrderTx.rawTransaction)
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

delegateCreateOrderTx = w3.eth.account.signTransaction(delegateCreateOrderTxRaw, admin01.key)
delegateCreateOrderTxhash = w3.eth.sendRawTransaction(delegateCreateOrderTx.rawTransaction)
print("create order:", delegateCreateOrderTxhash.hex())
time.sleep(10)

#####################
# cancle
stcohash = ZINKAllinone.functions.genActionHash(b"cancelorder",lastOrderId).call()
stcohex = "0x" + binascii.hexlify(stcohash).decode()
stcomsg = encode_defunct(hexstr=stcohex)
st01cosignature = w3.eth.account.sign_message(stcomsg, st01.privateKey)
st01cosighex = st01cosignature.signature.hex()


stcorawTx = ZINKAllinone.functions.ZINKAdminDelegateCancelOrder(lastOrderId, binascii.unhexlify(st01cosighex[2:])).buildTransaction(
    {
        'chainId': w3.eth.chain_id,
        'gas': 5 * 10 ** 6,
        'gasPrice': w3.eth.gas_price,
        'value': 0,
        'nonce': w3.eth.get_transaction_count(admin01.address),
        'from': admin01.address
    }
)
stcorawTxSigned = w3.eth.account.signTransaction(stcorawTx, admin01.key)
stcorawTxSignedHash = w3.eth.sendRawTransaction(stcorawTxSigned.rawTransaction)
print(stcorawTxSignedHash.hex())
time.sleep(10)

