


## contract api list

```
ZINKmarket
ADMIN_ROLE()
AcceptBidForOrder(uint256 order_id,uint256 bid_index)
DEFAULT_ADMIN_ROLE()
OWNER_ROLE()
OrderChangeToArbitration(uint256 order_id)
STUDENT_ROLE()
TEACHER_ROLE()
ViewOrderById(uint256 order_id)
ZINKAdminChangeOrderCID(uint256 order_id,string CID)
ZINKAdminChangeOrderURL(uint256 order_id,string question_url)
ZINKAdminDelegateAcceptBidForOrder(uint256 order_id,uint256 bid_index,address teacher_address,bytes sig)
ZINKAdminDelegateBidOrder(uint256 order_id,uint256 bid_amount,address teacher_address,bytes sig)
ZINKAdminDelegateCreateOrder(uint256 question_id,string question_url,string CID,bytes32 question_hash,address token_address,address student_address,bytes sig)
bid_the_order(uint256 order_id,uint256 bid_amount)
cancelOrderByOrderId(uint256 order_id)
cancelOrderByOrderIdWithOrderContract(uint256 order_id)
createOrder(uint256 question_id,string question_url,string CID,bytes32 question_hash,address token_address)
finishOrderByOrderId(uint256 order_id)
genDelegateAcceptBidForOrderHash(uint256 order_id,uint256 bid_index)
genDelegateBidOrderHash(uint256 order_id,uint256 bid_amount)
genDelegateCreateOrderHash(uint256 question_id,address token_address,bytes32 question_hash)
getRoleAdmin(bytes32 role)
grantRole(bytes32 role,address account)
hasRole(bytes32 role,address account)
orderIdToOrderContract(uint256 )
orders(uint256 )
packSignature(bytes32 r,bytes32 s,uint8 v)
recover(bytes32 hash,bytes sig)
recover(bytes32 hash,bytes32 r,bytes32 s,uint8 v)
renounceRole(bytes32 role,address account)
revokeAddressAdmin(address _address)
revokeRole(bytes32 role,address account)
setAddressAdmin(address _address)
supperAdmin()
supportsInterface(bytes4 interfaceId)
waitingAcceptOrderByOrderId(uint256 order_id)

-------------------

ZINKOrderContract
ADMIN_ROLE()
CID()
CancelOrder()
DEFAULT_ADMIN_ROLE()
OWNER_ROLE()
STUDENT_ROLE()
TEACHER_ROLE()
ZINKAdminDelegateCancelOrder()
ZINKAdminDelegateStudentAcceptOrder(bytes sig)
ZINKAdminDelegateTeacherFinishOrder(bytes sig)
adminSubmitFinalArbitrationResult(uint256 supportNum,uint256 opposeNum,address[3] VoterAddress,bytes[3] VoterSig,bytes AdminSig)
applyForArbitration(string claims)
bid_amount()
bid_idx()
genArbitrationHash(uint256 orderId,address orderContractAddress)
genStudentAcceptOrderHash(address studentAddress,uint256 orderId,uint256 questionId,uint256 bidAmount)
genteacherFinishOrderHash(address teacherAddress,uint256 orderId,uint256 questionId,uint256 bidAmount)
getRoleAdmin(bytes32 role)
grantRole(bytes32 role,address account)
hasRole(bytes32 role,address account)
initStepOne(address _token_address,bytes32 _question_hash,string _question_url,string _CID,uint256 _bid_idx)
order_id()
order_status()
question_hash()
question_id()
question_url()
recover(bytes32 hash,bytes sig)
recover(bytes32 hash,bytes32 r,bytes32 s,uint8 v)
renounceRole(bytes32 role,address account)
revokeRole(bytes32 role,address account)
studentAcceptOrder()
student_address()
supportsInterface(bytes4 interfaceId)
teacherFinishOrder()
teacher_address()
token_address()
zinkmarket()
```

## gas estimate
This is compiler estimate the function cost unit gas.
gasCost = gas * gasPrice;
infinite means compiler can not estimate the gas.
we will calculate gas by test Contract. (TODO)

ZINKOrderContract.sol
```
{
	"Creation": {
		"codeDepositCost": "2563400",
		"executionCost": "infinite",
		"totalCost": "infinite"
	},
	"External": {
		"ADMIN_ROLE()": "infinite",
		"CID()": "infinite",
		"CancelOrder()": "infinite",
		"DEFAULT_ADMIN_ROLE()": "284",
		"OWNER_ROLE()": "328",
		"STUDENT_ROLE()": "305",
		"TEACHER_ROLE()": "285",
		"ZINKAdminDelegateCancelOrder()": "infinite",
		"ZINKAdminDelegateStudentAcceptOrder(bytes)": "infinite",
		"ZINKAdminDelegateTeacherFinishOrder(bytes)": "infinite",
		"adminSubmitFinalArbitrationResult(uint256,uint256,address[3],bytes[3],bytes)": "infinite",
		"applyForArbitration(string)": "infinite",
		"bid_amount()": "2341",
		"bid_idx()": "2362",
		"genArbitrationHash(uint256,address)": "699",
		"genStudentAcceptOrderHash(address,uint256,uint256,uint256)": "720",
		"genteacherFinishOrderHash(address,uint256,uint256,uint256)": "741",
		"getRoleAdmin(bytes32)": "2560",
		"grantRole(bytes32,address)": "infinite",
		"hasRole(bytes32,address)": "2717",
		"initStepOne(address,bytes32,string,string,uint256)": "infinite",
		"order_id()": "2428",
		"order_status()": "2474",
		"question_hash()": "2361",
		"question_id()": "2340",
		"question_url()": "infinite",
		"recover(bytes32,bytes)": "infinite",
		"recover(bytes32,bytes32,bytes32,uint8)": "infinite",
		"renounceRole(bytes32,address)": "29128",
		"revokeRole(bytes32,address)": "infinite",
		"studentAcceptOrder()": "95358",
		"student_address()": "2381",
		"supportsInterface(bytes4)": "473",
		"teacherFinishOrder()": "4856",
		"teacher_address()": "2405",
		"token_address()": "2449",
		"zinkmarket()": "2449"
	}
}
```

ZINKmarket.sol
```
{
	"Creation": {
		"codeDepositCost": "5710400",
		"executionCost": "infinite",
		"totalCost": "infinite"
	},
	"External": {
		"ADMIN_ROLE()": "infinite",
		"AcceptBidForOrder(uint256,uint256)": "5390865",
		"DEFAULT_ADMIN_ROLE()": "284",
		"OWNER_ROLE()": "283",
		"OrderChangeToArbitration(uint256)": "31133",
		"STUDENT_ROLE()": "infinite",
		"TEACHER_ROLE()": "328",
		"ViewOrderById(uint256)": "infinite",
		"ZINKAdminChangeOrderCID(uint256,string)": "infinite",
		"ZINKAdminChangeOrderURL(uint256,string)": "infinite",
		"ZINKAdminDelegateAcceptBidForOrder(uint256,uint256,address,bytes)": "infinite",
		"ZINKAdminDelegateBidOrder(uint256,uint256,address,bytes)": "infinite",
		"ZINKAdminDelegateCreateOrder(uint256,string,string,bytes32,address,address,bytes)": "infinite",
		"bid_the_order(uint256,uint256)": "118595",
		"cancelOrderByOrderId(uint256)": "32138",
		"cancelOrderByOrderIdWithOrderContract(uint256)": "32160",
		"createOrder(uint256,string,string,bytes32,address)": "215611",
		"finishOrderByOrderId(uint256)": "31190",
		"genDelegateAcceptBidForOrderHash(uint256,uint256)": "566",
		"genDelegateBidOrderHash(uint256,uint256)": "586",
		"genDelegateCreateOrderHash(uint256,address,bytes32)": "692",
		"getRoleAdmin(bytes32)": "2493",
		"grantRole(bytes32,address)": "infinite",
		"hasRole(bytes32,address)": "2741",
		"orderIdToOrderContract(uint256)": "2589",
		"orders(uint256)": "infinite",
		"packSignature(bytes32,bytes32,uint8)": "infinite",
		"recover(bytes32,bytes)": "infinite",
		"recover(bytes32,bytes32,bytes32,uint8)": "infinite",
		"renounceRole(bytes32,address)": "29085",
		"revokeAddressAdmin(address)": "infinite",
		"revokeRole(bytes32,address)": "infinite",
		"setAddressAdmin(address)": "infinite",
		"supperAdmin()": "2382",
		"supportsInterface(bytes4)": "473",
		"waitingAcceptOrderByOrderId(uint256)": "31128"
	}
}
```




