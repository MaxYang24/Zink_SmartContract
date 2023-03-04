pragma solidity =0.8.17;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";


contract ZINKAnswerNFT is ERC721,AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OWNER_ROLE = keccak256("OWNER_ROLE");
    bytes32 public constant STUDENT_ROLE = keccak256("STUDENT_ROLE");
    bytes32 public constant TEACHER_ROLE = keccak256("TEACHER_ROLE");
    address public supperAdmin;


    mapping(uint => string) public answerCID;

    constructor() ERC721("ZINKAnswerNFT", "ZINKASNFT") public {
        supperAdmin = address(msg.sender);
        _setupRole(OWNER_ROLE, msg.sender);
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721, AccessControl) returns (bool) {
        return super.supportsInterface(interfaceId);
    }

    event setAddressAdminEvent(address _address);
    function setAddressAdmin(address _address) public {
        // require(hasRole(OWNER_ROLE, msg.sender), "Caller is not an owner");
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        _setupRole(ADMIN_ROLE, _address);
        emit setAddressAdminEvent(_address);
    }

    event revokeAddressAdminEvent(address _address);
    function revokeAddressAdmin(address _address) public {
        // require(hasRole(OWNER_ROLE, msg.sender), "Caller is not an owner");
        require(hasRole(OWNER_ROLE, msg.sender) == true, "not owner!");
        revokeRole(ADMIN_ROLE, _address);
        emit revokeAddressAdminEvent(_address);
    }

    function checkOriginIsAdmin() internal{
        require(hasRole(ADMIN_ROLE, tx.origin) == true, "not owner!");
    }

    function mintAnswerNFT(address to, uint orderId, string memory CID) public{
        checkOriginIsAdmin();
        _mint(to, orderId);
        //_setTokenURI(orderId, CID);
        answerCID[orderId] = CID;
    }

    function changeAnswerCID(uint orderId, string memory CID) public{
        checkOriginIsAdmin();
        answerCID[orderId] = CID;
    }

}
