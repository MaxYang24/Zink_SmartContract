// SPDX-License-Identifier: MIT
pragma solidity =0.8.17;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ZINKcoin is ERC20 {
    constructor() ERC20("ZINKcoin", "ZINK") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}
