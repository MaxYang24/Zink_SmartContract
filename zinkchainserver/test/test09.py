import requests
import time
import binascii
from web3 import Web3


tx_hash = "0xf09219162dd3499d828f22c6d695d4199bd4426f044e169722a2eed91266a78c"

def q(txh):
    url = "http://localhost:6666/querySmallContractAddrByTxHash"
    response = requests.post(url, json={"txhash": txh})
    assert response.status_code == 200
    ret = response.json()
    return ret

print(q(tx_hash))