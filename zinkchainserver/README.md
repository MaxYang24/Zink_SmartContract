# zinkserver chain server
## caution!
This server is only permitted to run on 127.0.0.1
## docs
### http://127.0.0.1:6666/docs
### all address and signature variables are hex string. They should start with "0x"
for example, "0x1EB91dc729092d2b8382A8A69b12b58B15ec7338", "0x2345676543212345676543212345676543234567654323456543234565432345676543"

### how student sign their hash
```
# teacher finish order
#    class genteacherFinishOrderHashItem(BaseModel):
#        cid: str
#        timeLimit: str
#        smallContractAdr: str
url = "http://127.0.0.1:6666/genteacherFinishOrderHash"
response = requests.post(url, json={"cid": cid, "timeLimit": limitTime, "smallContractAdr": smallContractAddress})
assert response.status_code == 200
ret = response.json()
print(ret)
message = encode_defunct(hexstr=ret["hash"])
tc01signature = w3.eth.account.sign_message(message, private_key=tc01.privateKey)
tc01sig = tc01signature.signature.hex()
print(tc01sig)
```
how front end engineers finish this function?
1. front end action transfer to main server. main server select the generate hash function, and request chain server to get the hashA.
2. main server send this hashA to client
3. front end invoke metamsk wallet program sign this message.
(sign message schema use EIP-712: Typed structured data hashing and signing.)
4. If you don't know what is EIP-712, just send hashA to prefixedHash API of chain server. hashB send to client.

client also can use the following codes to sign message.
```
message = encode_defunct(hexstr=HASH)
tc01signature = w3.eth.account.sign_message(message, private_key=tc01.privateKey)
tc01sig = tc01signature.signature.hex()
print(tc01sig)
```
w3.eth.account.sign_messag has already use EIP-712 standard. so HASH is hashA.


