pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MockWDAI is ERC20 {
    constructor() ERC20("Mock DAI", "DAI") {}
}
