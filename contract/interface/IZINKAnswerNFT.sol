pragma solidity =0.8.17;
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";


interface IZINKAnswerNFT is IERC721{

    function mintAnswerNFT(address to, uint orderId, string memory CID) external;

    function changeAnswerCID(uint orderId, string memory CID) external;
}