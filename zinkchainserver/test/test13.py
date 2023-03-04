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


url = "http://localhost:6666/ZINKControlledAccoutPrepareOrder"
response = requests.post(url, json={
    "question_id": "12344321",
    "question_url": "www.google.com",
    "CID": "www.us.com",
    "question_hash": "0x" + "3" * 32,
    "bid_amount": "1000",
    "limit_time": "23333"
    })
assert response.status_code == 200
ret = response.json()
txhash = ret["txhash"]
time.sleep(10)

url = "http://localhost:6666/queryTxPrepareOrderId"
response = requests.post(url, json={"txhash": txhash})
assert response.status_code == 200
ret = response.json()
order_id_onchain = ret["order_id_onchain"]
print(order_id_onchain)

url = "http://localhost:6666/ZINKControlledAccoutCreateOrder"
response = requests.post(url, json={"order_id_chain": order_id_onchain})
assert response.status_code == 200
ret = response.json()
print(ret)
time.sleep(10)

url = "http://localhost:6666/ZINKAdminDelegateApplyArbitratingOrder"
response = requests.post(url, json={"order_id_chain": order_id_onchain})
assert response.status_code == 200
ret = response.json()
print(ret)
time.sleep(10)

url = "http://localhost:6666/ZINKAdminDelegateSubmitFinalArbitrationResult"
response = requests.post(url, json={"order_id_chain": order_id_onchain, "v01isSupport": "0", "v02isSupport": "0", "v03isSupport": "0"})
assert response.status_code == 200
ret = response.json()
print(ret)
time.sleep(10)
