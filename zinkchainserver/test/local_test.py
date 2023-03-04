import requests
import time
import binascii
from web3 import Web3
from eth_account.messages import encode_defunct


w3 = Web3(Web3.HTTPProvider("https://polygon-mumbai.infura.io/v3/8e0e615d913549cab4693265bc1725d7"))
localstudent = w3.eth.account.from_key("7e5bfb82febc4c2c8529167104271ceec190eafdca277314912eaabdb67c6e5f")
hash_wait = "0xad3228b676f7d3cd4284a5443f17f1962b36e491b30a40b2405849e597ba5fb5"
message = encode_defunct(hexstr=hash_wait)
signature = w3.eth.account.sign_message(message, private_key=localstudent.privateKey)
sig = signature.signature.hex()
print(sig)

