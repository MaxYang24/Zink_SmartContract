# zink on-chain source codes

## Language: Python, Solidity
## Make sure you have the following packages downloaded:
fastapi, pydantic, web3, uvicorn, binascii, requests

## Contract descriptions

1. ZINKallinone.sol: handles most of the work, including creating orders, submitting answers, accepting answers, arbitration...
  - Functions:
    - Preperation:
      - setAnserNFTAddress: sets existing answer NFT addr
      - setFeeRation: sets handling fee rate
      - setAddressAdmin: sets admin addr
      - revokeAddressAdmin: revokes addmin
      - requireAdminAccess: checks if the caller is admin
      - viewOrder: input order information
      - prepareOrder: sets initial order instance vars
    - Hashing:
      - genActionHash: generates action hash
      - genArbitrateHash: generates arbitration hash
      - genCreatOrderHash: generates order creation hash
      - ...
    - Encoding:
      - recover
    - Orders:
      - unlockAnswer: unlocks previous answered questions
      - ZINKAdminDelegateCreateOrder: admin create order
      - ZINKAdminDelegateTeacherSubimitOrder: teacher submits answer
      - ZINKAdminDelegateStudentAcceptOrder: student accepts answer (triggers payment and nft minting)
      - ZINKAdminDelegateCancelOrder: admin cancels order
      - ZINKAdminDelegateApplyArbitratingOrder: change order status to arbitrating
      - ZINKAdminDelegateSubmitFinalArbitrationResult: final voting with selected reviewers signing and voting (check if supportnum >=2)
2. ZINKAnswerNFT.sol: in charge of all NFT stuff
  - Functions:
    - supportsInterface
    - setAddressAdmin: sets admin addr
    - revokeAddressAdmin: revokes addmin
    - checkOriginIsAdmin: checks if owner
    - mintAnswerNFT: mint answer NFT
    - changeAnswerCID: sets and changes answer NFT CID    

### How to use smart contracts?
just run python ./zinkchainserver/src/main.py, it will startup a server for testing purpose

## When the server is running, open a side terminal tab and run the following tests to check if the contracts are behaving correctly

### Tests: the tests in ./zinkchainserver/test/ test for main functions:
  - test10 - Request order info and status by order_id
  - test11 - Create order -> submit answer -> finish order
  - test12 - Create order -> cancel order -> finish order
  - test11 - Create order -> submit answer -> arbitration -> finish order

