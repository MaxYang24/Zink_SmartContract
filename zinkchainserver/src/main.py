from fastapi import FastAPI
from zinkconfig import zinkcoin, zinkallinone, zinkanswernft
from pydantic import BaseModel
from web3 import Web3
import os
import uvicorn
import binascii
from eth_account.messages import encode_defunct


w3 = Web3(Web3.HTTPProvider(
    "https://polygon-mumbai.g.alchemy.com/v2/-dSjCpSmQAIk3nwZ45vNsBxg1DMydqK5"))
assert w3.isConnected(), "Not connected to Ethereum node"
admin01key = open(os.path.dirname(os.path.abspath(__file__)) +
                  "/../admin_key/admin01privatekey.txt", "r").read()
admin01 = w3.eth.account.from_key(admin01key)
print("admin address: ", admin01.address)

st01key = open(os.path.dirname(os.path.abspath(__file__)) +
               "/../admin_key/st01privatekey.txt", "r").read()
st01 = w3.eth.account.from_key(st01key)
print("student address is ", st01.address)

tc01key = open(os.path.dirname(os.path.abspath(__file__)) +
               "/../admin_key/tc01privatekey.txt", "r").read()
tc01 = w3.eth.account.from_key(tc01key)
print("teacher address is ", tc01.address)

arb1key = open(os.path.dirname(os.path.abspath(__file__)) +
               "/../admin_key/arb1key.txt", "r").read()
arb1 = w3.eth.account.from_key(arb1key)

arb2key = open(os.path.dirname(os.path.abspath(__file__)) +
               "/../admin_key/arb2key.txt", "r").read()
arb2 = w3.eth.account.from_key(arb2key)

arb3key = open(os.path.dirname(os.path.abspath(__file__)) +
               "/../admin_key/arb3key.txt", "r").read()
arb3 = w3.eth.account.from_key(arb3key)


ZINKCoin = w3.eth.contract(address=w3.toChecksumAddress(zinkcoin), abi=open(os.path.dirname(
    os.path.abspath(__file__)) + "/../contract_abi/ZINKCoin.json", "r").read())
ZINKAllinone = w3.eth.contract(address=w3.toChecksumAddress(zinkallinone), abi=open(os.path.dirname(
    os.path.abspath(__file__)) + "/../contract_abi/ZINKallinone.json", "r").read())
ZINKAnswerNFT = w3.eth.contract(address=w3.toChecksumAddress(zinkanswernft), abi=open(os.path.dirname(
    os.path.abspath(__file__)) + "/../contract_abi/ZINKAnswerNFT.json", "r").read())

app = FastAPI()


class viewOrderItem(BaseModel):
    order_id_chain: str


# ORDER_STATUS{cancelled, finished, arbitrating, ongoing, waitingAccept, preparing}
ORDER_STATUS = {
    0: "cancelled",
    1: "finished",
    2: "arbitrating",
    3: "ongoing",
    4: "waitingAccept",
    5: "preparing"
}


@app.post("/viewOrder")
def viewOrder(item: viewOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        infoTuple = ZINKAllinone.functions.viewOrder(order_id_chain).call()
        order_id_chain_, studentAddr, teacherAddr, order_status, CID, question_url, question_id, question_hash, bid_amount, limit_time, start_time = infoTuple
        retJson = {}
        retJson["order_id_chain"] = order_id_chain_
        retJson["studentAddr"] = studentAddr
        retJson["teacherAddr"] = teacherAddr
        retJson["order_status"] = ORDER_STATUS[order_status]
        retJson["CID"] = CID
        retJson["question_url"] = question_url
        retJson["question_id"] = question_id
        retJson["question_hash"] = question_hash
        retJson["bid_amount"] = bid_amount
        retJson["limit_time"] = limit_time
        retJson["start_time"] = start_time
        return retJson
    except Exception:
        return {"error": "some errors"}

# struct orderInfo {
#     uint question_id;
#     address student_address;
#     string question_url;
#     string CID;
#     bytes32 question_hash;
#     ORDER_STATUS order_status;
#     uint order_id_chain;
#     uint bid_amount;
#     address teacher_address;
#     uint limit_time; // second;
#     uint start_time;
# }


class prepareOrderItem(BaseModel):
    question_id: str
    student_address: str
    question_url: str
    CID: str
    question_hash: str
    bid_amount: str
    teacher_address: str
    limit_time: str


class ZINKControlledAccoutprepareOrderItem(BaseModel):
    question_id: str
    question_url: str
    CID: str
    question_hash: str
    bid_amount: str
    limit_time: str


@app.post("/ZINKControlledAccoutPrepareOrder")
def ZINKControlledAccoutPrepareOrder(item: ZINKControlledAccoutprepareOrderItem):
    try:
        question_id = int(item.question_id)
        # student_address = w3.toChecksumAddress(item.student_address)
        student_address = st01.address
        question_url = item.question_url
        CID = item.CID
        assert item.question_hash[:2] == "0x"
        question_hash = binascii.unhexlify(item.question_hash[2:])
        bid_amount = int(item.bid_amount)
        # teacher_address = w3.toChecksumAddress(item.teacher_address)
        teacher_address = tc01.address
        limit_time = int(item.limit_time)
        prepareOrderTxRaw = ZINKAllinone.functions.prepareOrder([question_id, student_address, question_url, CID, question_hash, 0, 0, bid_amount, teacher_address, limit_time, 0]).buildTransaction(
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
        txHash = signedPrepareOrderTxhash.hex()
        return {"txhash": txHash}
    except Exception:
        return {"error": "errors"}


class txhash(BaseModel):
    txhash: str


@app.post("/queryTxPrepareOrderId")
def queryTxPrepareOrderId(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.PrepareOrder().processReceipt(thisReceipt)
        return {"order_id_onchain": logs[0].args.order_id_onchain}
    except Exception:
        return {"error": "errors"}


@app.post("/queryTxCreateOrderId")
def queryTxCreateOrderId(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.CreateOrder().processReceipt(thisReceipt)
        return {"order_id_chain": logs[0].args.order_id_chain}
    except Exception:
        return {"error": "errors"}


@app.post("/queryTxSubmitOrder")
def queryTxSubmitOrder(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.SubmitOrder().processReceipt(thisReceipt)
        return {"order_id_chain": logs[0].args.order_id_chain}
    except Exception:
        return {"error": "errors"}


@app.post("/queryTxAcceptOrder")
def queryTxAcceptOrder(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.AcceptOrder().processReceipt(thisReceipt)
        return {"order_id_chain": logs[0].args.order_id_chain}
    except Exception:
        return {"error": "errors"}


@app.post("/queryTxCancleOrder")
def queryTxCancleOrder(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.CancleOrder().processReceipt(thisReceipt)
        return {"order_id_chain": logs[0].args.order_id_chain}
    except Exception:
        return {"error": "errors"}


@app.post("/queryTxArbitrateOrder")
def queryTxArbitrateOrder(item: txhash):
    try:
        txhashi = item.txhash
        thisReceipt = w3.eth.get_transaction_receipt(txhashi)
        logs = ZINKAllinone.events.ArbitrateOrder().processReceipt(thisReceipt)
        return {"order_id_chain": logs[0].args.order_id_chain}
    except Exception:
        return {"error": "errors"}


class ZINKControlledAccoutCreateOrderItem(BaseModel):
    order_id_chain: str


@app.post("/ZINKControlledAccoutCreateOrder")
def ZINKControlledAccoutCreateOrder(item: ZINKControlledAccoutCreateOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        OrderHash = ZINKAllinone.functions.genCreatOrderHash(
            order_id_chain).call()
        message = encode_defunct(hexstr=OrderHash.hex())
        st01signature = w3.eth.account.sign_message(message, st01.privateKey)
        st01sig = st01signature.signature.hex()
        message = encode_defunct(hexstr=OrderHash.hex())
        tc01signature = w3.eth.account.sign_message(message, tc01.privateKey)
        tc01sig = tc01signature.signature.hex()
        delegateCreateOrderTxRaw = ZINKAllinone.functions.ZINKAdminDelegateCreateOrder(order_id_chain, binascii.unhexlify(st01sig[2:]), binascii.unhexlify(tc01sig[2:])).buildTransaction(
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
        return {"txhash": delegateCreateOrderTxhash.hex()}
    except Exception:
        return {"error": "errors"}

# ZINKAdminDelegateTeacherSubimitOrder


class ZINKControlledAccoutDelegateTeacherSubimitOrderItem(BaseModel):
    order_id_chain: str
    newCID: str


@app.post("/ZINKControlledAccoutDelegateTeacherSubimitOrder")
def ZINKControlledAccoutDelegateTeacherSubimitOrder(item: ZINKControlledAccoutDelegateTeacherSubimitOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        newCID = item.newCID
        sahash = ZINKAllinone.functions.genActionHash(
            b"submitanswer", order_id_chain).call()
        sahex = "0x" + binascii.hexlify(sahash).decode()
        samsg = encode_defunct(hexstr=sahex)
        tc01sasignature = w3.eth.account.sign_message(samsg, tc01.privateKey)
        tc01sighex = tc01sasignature.signature.hex()
        tcsubrawTx = ZINKAllinone.functions.ZINKAdminDelegateTeacherSubimitOrder(order_id_chain, binascii.unhexlify(tc01sighex[2:]), newCID).buildTransaction(
            {
                'chainId': w3.eth.chain_id,
                'gas': 5 * 10 ** 6,
                'gasPrice': w3.eth.gas_price,
                'value': 0,
                'nonce': w3.eth.get_transaction_count(admin01.address),
                'from': admin01.address
            }
        )
        tcsubrawTxSigned = w3.eth.account.signTransaction(
            tcsubrawTx, admin01.key)
        tcsubrawTxSignedTxhash = w3.eth.sendRawTransaction(
            tcsubrawTxSigned.rawTransaction)
        return {"txhash": tcsubrawTxSignedTxhash.hex()}
    except Exception:
        return {"error": "errors"}


class ZINKAddressIsUnlockContentItem(BaseModel):
    order_id_chain: str
    unlockAddress: str


@app.post("/ZINKAddressIsUnlockContent")
def ZINKAddressIsUnlockContent(item: ZINKAddressIsUnlockContentItem):
    try:
        order_id_chain = int(item.order_id_chain)
        unlockAddress = w3.toChecksumAddress(item.unlockAddress)
        ret = ZINKAllinone.functions.unlockAnswerRecord(
            order_id_chain, unlockAddress).call()
        retStr = ""
        if ret == 0:
            retStr = "not unlocked"
        else:
            retStr = "unlocked"
        return {"isUnlockAddress": str(ret), "result": retStr}
    except Exception:
        return {"error": "errors"}


class ZINKControlledAccoutStudentAcceptOrderItem(BaseModel):
    order_id_chain: str


@app.post("/ZINKControlledAccoutStudentAcceptOrder")
def ZINKControlledAccoutStudentAcceptOrder(item: ZINKControlledAccoutStudentAcceptOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        aahash = ZINKAllinone.functions.genActionHash(
            b"accpetanswer", order_id_chain).call()
        aahex = "0x" + binascii.hexlify(aahash).decode()
        aamsg = encode_defunct(hexstr=aahex)
        st01aasignature = w3.eth.account.sign_message(aamsg, st01.privateKey)
        st01sighex = st01aasignature.signature.hex()
        staarawTx = ZINKAllinone.functions.ZINKAdminDelegateStudentAcceptOrder(order_id_chain, binascii.unhexlify(st01sighex[2:])).buildTransaction(
            {
                'chainId': w3.eth.chain_id,
                'gas': 5 * 10 ** 6,
                'gasPrice': w3.eth.gas_price,
                'value': 0,
                'nonce': w3.eth.get_transaction_count(admin01.address),
                'from': admin01.address
            }
        )
        staarawTxSigned = w3.eth.account.signTransaction(
            staarawTx, admin01.key)
        staarawTxSignedTxhash = w3.eth.sendRawTransaction(
            staarawTxSigned.rawTransaction)
        return {"txhash": staarawTxSignedTxhash.hex()}
    except Exception:
        return {"error": "errors"}


class ZINKControlledAccoutStudentCancelOrderItem(BaseModel):
    order_id_chain: str


@app.post("/ZINKControlledAccoutStudentCancelOrder")
def ZINKControlledAccoutStudentCancelOrder(item: ZINKControlledAccoutStudentCancelOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        stcohash = ZINKAllinone.functions.genActionHash(
            b"cancelorder", order_id_chain).call()
        stcohex = "0x" + binascii.hexlify(stcohash).decode()
        stcomsg = encode_defunct(hexstr=stcohex)
        st01cosignature = w3.eth.account.sign_message(stcomsg, st01.privateKey)
        st01cosighex = st01cosignature.signature.hex()
        stcorawTx = ZINKAllinone.functions.ZINKAdminDelegateCancelOrder(order_id_chain, binascii.unhexlify(st01cosighex[2:])).buildTransaction(
            {
                'chainId': w3.eth.chain_id,
                'gas': 5 * 10 ** 6,
                'gasPrice': w3.eth.gas_price,
                'value': 0,
                'nonce': w3.eth.get_transaction_count(admin01.address),
                'from': admin01.address
            }
        )
        stcorawTxSigned = w3.eth.account.signTransaction(
            stcorawTx, admin01.key)
        stcorawTxSignedHash = w3.eth.sendRawTransaction(
            stcorawTxSigned.rawTransaction)
        return {"txhash": stcorawTxSignedHash.hex()}
    except Exception:
        return {"error": "errors"}


class ZINKAdminDelegateApplyArbitratingOrderItem(BaseModel):
    order_id_chain: str


@app.post("/ZINKAdminDelegateApplyArbitratingOrder")
def ZINKAdminDelegateApplyArbitratingOrder(item: ZINKAdminDelegateApplyArbitratingOrderItem):
    try:
        order_id_chain = int(item.order_id_chain)
        DelegateArbitrateOrderRawTx = ZINKAllinone.functions.ZINKAdminDelegateApplyArbitratingOrder(order_id_chain).buildTransaction(
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
        return {"txhash": DelegateArbitrateOrderTxhash.hex()}
    except Exception:
        return {"error": "errors"}


class ZINKgenArbitrateHashItem(BaseModel):
    isSupport: str
    order_id_chain: str


@app.post("/ZINKgenArbitrateHash")
def ZINKgenArbitrateHash(item: ZINKgenArbitrateHashItem):
    try:
        isSupport = int(item.isSupport)
        order_id_chain = int(item.order_id_chain)
        retHash = ZINKAllinone.functions.genArbitrateHash(
            isSupport, order_id_chain).call()
        return {"hash": "0x" + binascii.hexlify(retHash)}
    except Exception:
        return {"error": "errors"}


class ZINKAdminDelegateSubmitFinalArbitrationResultItem(BaseModel):
    order_id_chain: str
    v01isSupport: str
    v02isSupport: str
    v03isSupport: str
    # v01: str
    # v02: str
    # v03: str
    # v01sig: str
    # v02sig: str
    # v03sig: str


@app.post("/ZINKAdminDelegateSubmitFinalArbitrationResult")
def ZINKAdminDelegateSubmitFinalArbitrationResult(item: ZINKAdminDelegateSubmitFinalArbitrationResultItem):
    try:
        order_id_chain = int(item.order_id_chain)
        v01isSupport = int(item.v01isSupport)
        v02isSupport = int(item.v02isSupport)
        v03isSupport = int(item.v03isSupport)

        #
        v01supportHash = ZINKAllinone.functions.genArbitrateHash(
            v01isSupport, order_id_chain).call()
        oneM = encode_defunct(hexstr=v01supportHash.hex())
        v01signature = w3.eth.account.sign_message(oneM, arb1.privateKey)
        v01sig = v01signature.signature.hex()
        v01sig = binascii.unhexlify(v01sig[2:])
        v01 = w3.toChecksumAddress(arb1.address)

        v02supportHash = ZINKAllinone.functions.genArbitrateHash(
            v02isSupport, order_id_chain).call()
        twoM = encode_defunct(hexstr=v02supportHash.hex())
        v02signature = w3.eth.account.sign_message(twoM, arb2.privateKey)
        v02sig = v02signature.signature.hex()
        v02sig = binascii.unhexlify(v02sig[2:])
        v02 = w3.toChecksumAddress(arb2.address)

        v03supportHash = ZINKAllinone.functions.genArbitrateHash(
            v03isSupport, order_id_chain).call()
        threeM = encode_defunct(hexstr=v03supportHash.hex())
        v03signature = w3.eth.account.sign_message(threeM, arb3.privateKey)
        v03sig = v03signature.signature.hex()
        v03sig = binascii.unhexlify(v03sig[2:])
        v03 = w3.toChecksumAddress(arb3.address)

        sfarTxRaw = ZINKAllinone.functions.ZINKAdminDelegateSubmitFinalArbitrationResult(order_id_chain, [v01isSupport, v02isSupport, v03isSupport, v01, v02, v03, v01sig, v02sig, v03sig]).buildTransaction(
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
        sfarTxSignedHash = w3.eth.sendRawTransaction(
            sfarTxSigned.rawTransaction)
        return {"txhash": sfarTxSignedHash.hex()}
    except Exception:
        return {"error": "errors"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=6666)
