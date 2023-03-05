// SPDX-License-Identifier: MIT
pragma solidity =0.8.17;
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./interface/IZINKAnswerNFT.sol";

contract ZINKallinone is AccessControl, ReentrancyGuard {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OWNER_ROLE = keccak256("OWNER_ROLE");
    bytes32 public constant STUDENT_ROLE = keccak256("STUDENT_ROLE");
    bytes32 public constant TEACHER_ROLE = keccak256("TEACHER_ROLE");
    address public supperAdmin;
    uint256 public FeeRatio;
    uint256 immutable onethundreds = 1000;
    // x / 1000
    ERC20 public ZINK;
    IZINKAnswerNFT public AnswerNFT;
    mapping(uint256 => mapping(address => uint256)) public unlockAnswerRecord;

    // unlocks previous answered questions
    function unlockAnswer(uint256 order_id_chain, address unlockAddress)
        public
    {
        require(
            orders[order_id_chain].order_status == ORDER_STATUS.finished,
            "incorrect status"
        );
        address answerOwner = AnswerNFT.ownerOf(order_id_chain);
        {
            uint256 t1 = ZINK.balanceOf(address(this));
            ZINK.transferFrom(
                unlockAddress,
                address(this),
                orders[order_id_chain].bid_amount
            );
            uint256 t2 = ZINK.balanceOf(address(this));
            require(
                t2 == t1 + orders[order_id_chain].bid_amount,
                "receive money failed"
            );
        }
        {
            uint256 allFee = orders[order_id_chain].bid_amount;
            uint256 serviceFee = (allFee * FeeRatio) / onethundreds;
            uint256 remain = allFee - serviceFee;
            uint256 t1 = ZINK.balanceOf(address(supperAdmin));
            ZINK.approve(address(supperAdmin), serviceFee);
            ZINK.transfer(address(supperAdmin), serviceFee);
            uint256 t2 = ZINK.balanceOf(address(supperAdmin));
            require(t2 == t1 + serviceFee, "receive money failed");

            t1 = ZINK.balanceOf(address(answerOwner));
            ZINK.approve(address(answerOwner), remain);
            ZINK.transfer(address(answerOwner), remain);
            t2 = ZINK.balanceOf(address(answerOwner));
            require(t2 == t1 + remain, "receive money failed");
        }
        unlockAnswerRecord[order_id_chain][unlockAddress] = 1;
    }

    constructor(ERC20 zink_address, uint256 fee_) public {
        _setupRole(OWNER_ROLE, msg.sender);
        supperAdmin = msg.sender;
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        ZINK = zink_address;
        FeeRatio = fee_;
    }

    // sets existing answer NFT addr
    function setAnserNFTAddress(address a) public {
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        AnswerNFT = IZINKAnswerNFT(a);
    }

    event setFee(uint256 _value);

    // sets handling fee rate
    function setFeeRation(uint256 newFeeRatio) public {
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        FeeRatio = newFeeRatio;
        emit setFee(newFeeRatio);
    }

    event setAddressAdminEvent(address _address);

    // sets admin addr
    function setAddressAdmin(address _address) public {
        // require(hasRole(OWNER_ROLE, msg.sender), "Caller is not an owner");
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        _setupRole(ADMIN_ROLE, _address);
        emit setAddressAdminEvent(_address);
    }

    event revokeAddressAdminEvent(address _address);

    // revokes addmin
    function revokeAddressAdmin(address _address) public {
        // require(hasRole(OWNER_ROLE, msg.sender), "Caller is not an owner");
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        revokeRole(ADMIN_ROLE, _address);
        emit revokeAddressAdminEvent(_address);
    }

    enum ORDER_STATUS {
        cancelled,
        finished,
        arbitrating,
        ongoing,
        waitingAccept,
        preparing
    }

    struct orderInfo {
        uint256 question_id;
        address student_address;
        string question_url;
        string CID;
        bytes32 question_hash;
        ORDER_STATUS order_status;
        uint256 order_id_chain;
        uint256 bid_amount;
        address teacher_address;
        uint256 limit_time; // second;
        uint256 start_time;
    }
    mapping(uint256 => orderInfo) public orders;
    uint256 public orderNum;

    // checks if the caller is admin
    function requireAdminAccess() internal {
        require(hasRole(ADMIN_ROLE, msg.sender), "Caller is not an admin");
    }

    // input order information
    function viewOrder(uint256 order_id_chain)
        public
        view
        returns (
            uint256 order_id_chain_,
            address studentAddr,
            address teacherAddr,
            ORDER_STATUS order_status,
            string memory CID,
            string memory question_url,
            uint256 question_id,
            bytes32 question_hash,
            uint256 bid_amount,
            uint256 limit_time,
            uint256 start_time
        )
    {
        orderInfo storage this_order = orders[order_id_chain];
        order_id_chain_ = this_order.order_id_chain;
        studentAddr = this_order.student_address;
        teacherAddr = this_order.teacher_address;
        order_status = this_order.order_status;
        CID = this_order.CID;
        question_url = this_order.question_url;
        question_id = this_order.question_id;
        question_hash = this_order.question_hash;
        bid_amount = this_order.bid_amount;
        limit_time = this_order.limit_time;
        start_time = this_order.start_time;
    }

    event PrepareOrder(uint256 order_id_onchain);

    // sets initial order instance vars
    function prepareOrder(orderInfo memory inputInfo) public nonReentrant {
        requireAdminAccess();
        orderInfo storage this_order = orders[orderNum];
        this_order.bid_amount = inputInfo.bid_amount;
        this_order.order_id_chain = orderNum;
        this_order.question_id = inputInfo.question_id;
        this_order.student_address = inputInfo.student_address;
        this_order.question_url = inputInfo.question_url;
        this_order.CID = inputInfo.CID;
        this_order.question_hash = inputInfo.question_hash;
        this_order.order_status = ORDER_STATUS.preparing;
        this_order.teacher_address = inputInfo.teacher_address;
        this_order.limit_time = inputInfo.limit_time;
        emit PrepareOrder(orderNum);
        orderNum += 1;
    }

    // generates action hash
    function genActionHash(string memory act, uint256 order_id_chain)
        public
        returns (bytes32 ret)
    {
        ret = keccak256(abi.encodePacked(act, order_id_chain));
    }

    // generates arbitration hash
    function genArbitrateHash(uint256 isSupport, uint256 order_id_chain)
        public
        returns (bytes32 ret)
    {
        ret = keccak256(abi.encodePacked(isSupport, order_id_chain));
    }

    // generates order creation hash
    function genCreatOrderHash(uint256 order_id_chain)
        public
        returns (bytes32 ret)
    {
        orderInfo memory this_order = orders[order_id_chain];
        ret = keccak256(
            abi.encodePacked(
                this_order.question_id,
                this_order.student_address,
                this_order.question_url,
                this_order.question_hash,
                this_order.order_id_chain,
                this_order.bid_amount,
                this_order.teacher_address
            )
        );
    }

    function prefixedHash(bytes32 hash) public view returns (bytes32) {
        return
            keccak256(
                abi.encodePacked("\x19Ethereum Signed Message:\n32", hash)
            );
    }

    function recover(bytes32 hash, bytes memory sig)
        public
        pure
        returns (address)
    {
        bytes32 r;
        bytes32 s;
        uint8 v;
        //Check the signature length
        if (sig.length != 65) {
            return (address(0));
        }

        // Divide the signature in r, s and v variables
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }

        // Version of signature should be 27 or 28, but 0 and 1 are also possible versions
        if (v < 27) {
            v += 27;
        }

        // If the version is correct return the signer address
        if (v != 27 && v != 28) {
            return (address(0));
        } else {
            return ecrecover(hash, v, r, s);
        }
    }

    event CreateOrder(uint256 order_id_chain);

    function ZINKAdminDelegateCreateOrder(
        uint256 order_id_chain,
        bytes memory studentSig,
        bytes memory teacherSig
    ) public nonReentrant {
        requireAdminAccess();
        require(
            orders[order_id_chain].order_status == ORDER_STATUS.preparing,
            "not preparing order"
        );
        bytes32 orderHash = prefixedHash(genCreatOrderHash(order_id_chain));
        require(
            recover(orderHash, studentSig) ==
                orders[order_id_chain].student_address,
            "not student sig!"
        );
        require(
            recover(orderHash, teacherSig) ==
                orders[order_id_chain].teacher_address,
            "not teacher sig!"
        );
        {
            uint256 before_balance = ZINK.balanceOf(address(this));
            ZINK.transferFrom(
                orders[order_id_chain].student_address,
                address(this),
                orders[order_id_chain].bid_amount
            );
            uint256 after_balance = ZINK.balanceOf(address(this));
            require(
                after_balance - before_balance >=
                    orders[order_id_chain].bid_amount,
                "transferFrom failed"
            );
        }
        orders[order_id_chain].start_time = block.timestamp;
        orders[order_id_chain].order_status = ORDER_STATUS.ongoing;
        emit CreateOrder(order_id_chain);
    }

    event SubmitOrder(uint256 order_id_chain);
    event ArbitrateOrder(uint256 order_id_chain);

    // teacher submits answer
    function ZINKAdminDelegateTeacherSubimitOrder(
        uint256 order_id_chain,
        bytes memory teacherSig,
        string memory newCID
    ) public nonReentrant {
        requireAdminAccess();
        bytes32 actionHash = prefixedHash(
            genActionHash("submitanswer", order_id_chain)
        );
        require(
            recover(actionHash, teacherSig) ==
                orders[order_id_chain].teacher_address
        );
        require(
            orders[order_id_chain].order_status == ORDER_STATUS.ongoing,
            "order status error"
        );
        if (
            block.timestamp - orders[order_id_chain].start_time <=
            orders[order_id_chain].limit_time
        ) {
            orderInfo storage this_order = orders[order_id_chain];
            this_order.order_status = ORDER_STATUS.waitingAccept;
            this_order.CID = newCID;
            emit SubmitOrder(order_id_chain);
        } else {
            orderInfo storage this_order = orders[order_id_chain];
            this_order.order_status = ORDER_STATUS.arbitrating;
            emit ArbitrateOrder(order_id_chain);
        }
    }

    event AcceptOrder(uint256 order_id_chain);

    // student accepts answer (triggers payment and nft minting)
    function ZINKAdminDelegateStudentAcceptOrder(
        uint256 order_id_chain,
        bytes memory studentSig
    ) public nonReentrant {
        requireAdminAccess();
        orderInfo storage this_order = orders[order_id_chain];
        require(
            this_order.order_status == ORDER_STATUS.waitingAccept,
            "order status error"
        );
        bytes32 actionHash = prefixedHash(
            genActionHash("accpetanswer", order_id_chain)
        );
        require(
            recover(actionHash, studentSig) ==
                orders[order_id_chain].student_address
        );
        this_order.order_status = ORDER_STATUS.finished;
        {
            uint256 allFee = this_order.bid_amount;
            uint256 serviceFee = (allFee * FeeRatio) / onethundreds;
            uint256 remain = allFee - serviceFee;
            uint256 before_balance = ZINK.balanceOf(address(this));
            ZINK.approve(this_order.teacher_address, remain);
            ZINK.transfer(this_order.teacher_address, this_order.bid_amount);
            uint256 after_balance = ZINK.balanceOf(address(this));
            require(
                before_balance == this_order.bid_amount + after_balance,
                "transfer failed"
            );
            AnswerNFT.mintAnswerNFT(
                this_order.teacher_address,
                this_order.order_id_chain,
                this_order.CID
            );
        }
        emit AcceptOrder(order_id_chain);
    }

    event CancleOrder(uint256 order_id_chain);

    // admin cancels order
    function ZINKAdminDelegateCancelOrder(
        uint256 order_id_chain,
        bytes memory studentSig
    ) public nonReentrant {
        requireAdminAccess();
        orderInfo storage this_order = orders[order_id_chain];
        bytes32 actionHash = prefixedHash(
            genActionHash("cancelorder", order_id_chain)
        );
        require(
            recover(actionHash, studentSig) ==
                orders[order_id_chain].student_address
        );
        require(
            this_order.order_status == ORDER_STATUS.ongoing,
            "order status error"
        );
        this_order.order_status = ORDER_STATUS.cancelled;
        {
            uint256 before_balance = ZINK.balanceOf(address(this));
            ZINK.approve(this_order.student_address, this_order.bid_amount);
            ZINK.transfer(this_order.student_address, this_order.bid_amount);
            uint256 after_balance = ZINK.balanceOf(address(this));
            require(
                before_balance == this_order.bid_amount + after_balance,
                "transfer failed"
            );
        }
        emit CancleOrder(order_id_chain);
    }

    // change order status to arbitrating
    function ZINKAdminDelegateApplyArbitratingOrder(uint256 order_id_chain)
        public
        nonReentrant
    {
        requireAdminAccess();
        orderInfo storage this_order = orders[order_id_chain];
        require(
            this_order.order_status == ORDER_STATUS.ongoing ||
                this_order.order_status == ORDER_STATUS.waitingAccept,
            "order status error"
        );
        this_order.order_status = ORDER_STATUS.arbitrating;
        emit ArbitrateOrder(order_id_chain);
    }

    struct arbitratingInfo {
        uint256 v01isSupport;
        uint256 v02isSupport;
        uint256 v03isSupport;
        address v01;
        address v02;
        address v03;
        bytes v01sig;
        bytes v02sig;
        bytes v03sig;
    }

    event ArbitrateResult(uint256 order_id_chain, string result);

    // final voting with selected reviewers signing and voting (check if supportnum >=2)
    function ZINKAdminDelegateSubmitFinalArbitrationResult(
        uint256 order_id_chain,
        arbitratingInfo memory info
    ) public nonReentrant {
        uint256 supportNum;
        uint256 opposeNum;
        require(
            info.v01isSupport <= 1 &&
                info.v02isSupport <= 1 &&
                info.v03isSupport <= 1,
            "support num is rong!"
        );
        requireAdminAccess();
        require(
            orders[order_id_chain].order_status == ORDER_STATUS.arbitrating,
            "order not arbitrating!"
        );
        bytes32 aimHash = prefixedHash(
            genArbitrateHash(info.v01isSupport, order_id_chain)
        );
        require(
            recover(aimHash, info.v01sig) == info.v01,
            "01 address invalid"
        );

        aimHash = prefixedHash(
            genArbitrateHash(info.v02isSupport, order_id_chain)
        );
        require(
            recover(aimHash, info.v02sig) == info.v02,
            "02 address invalid"
        );

        aimHash = prefixedHash(
            genArbitrateHash(info.v03isSupport, order_id_chain)
        );
        require(
            recover(aimHash, info.v03sig) == info.v03,
            "03 address invalid"
        );

        if (info.v01isSupport == 1) {
            supportNum += 1;
        } else {
            opposeNum += 1;
        }
        if (info.v02isSupport == 1) {
            supportNum += 1;
        } else {
            opposeNum += 1;
        }
        if (info.v03isSupport == 1) {
            supportNum += 1;
        } else {
            opposeNum += 1;
        }
        if (
            (supportNum == 3 && opposeNum == 0) ||
            (supportNum == 2 && opposeNum == 1)
        ) {
            orders[order_id_chain].order_status = ORDER_STATUS.finished;
            uint256 serviceFee = (orders[order_id_chain].bid_amount *
                FeeRatio) / onethundreds;
            uint256 teacherAmount = orders[order_id_chain].bid_amount -
                serviceFee;
            ZINK.approve(supperAdmin, serviceFee);
            uint256 t1 = ZINK.balanceOf(supperAdmin);
            ZINK.transfer(supperAdmin, serviceFee);
            uint256 t2 = ZINK.balanceOf(supperAdmin);
            require(t2 - t1 >= serviceFee, "not receive service fee");

            ZINK.approve(orders[order_id_chain].teacher_address, teacherAmount);
            t1 = ZINK.balanceOf(orders[order_id_chain].teacher_address);
            ZINK.transfer(
                orders[order_id_chain].teacher_address,
                teacherAmount
            );
            t2 = ZINK.balanceOf(orders[order_id_chain].teacher_address);
            require(t2 - t1 == teacherAmount, "teacher not receive fee");
            AnswerNFT.mintAnswerNFT(
                orders[order_id_chain].teacher_address,
                orders[order_id_chain].order_id_chain,
                orders[order_id_chain].CID
            );
            emit ArbitrateResult(order_id_chain, "teacher win");
        } else if (
            (supportNum == 0 && opposeNum == 3) ||
            (supportNum == 1 && opposeNum == 2)
        ) {
            orders[order_id_chain].order_status = ORDER_STATUS.finished;
            ZINK.approve(
                orders[order_id_chain].student_address,
                orders[order_id_chain].bid_amount
            );
            uint256 t1 = ZINK.balanceOf(orders[order_id_chain].student_address);
            ZINK.transfer(
                orders[order_id_chain].student_address,
                orders[order_id_chain].bid_amount
            );
            uint256 t2 = ZINK.balanceOf(orders[order_id_chain].student_address);
            require(t2 - t1 == orders[order_id_chain].bid_amount);
            emit ArbitrateResult(order_id_chain, "student refund");
        } else {
            require(1 == 2, "?");
        }
    }
}
