import requests
import time
import binascii
from web3 import Web3


def q(id):
    url = "http://localhost:6666/viewOrder"
    response = requests.post(url, json={"order_id_chain": id})
    assert response.status_code == 200
    ret = response.json()
    return ret

print(q(0))