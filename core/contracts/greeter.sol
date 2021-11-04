pragma solidity >=0.7.0 <0.9.0;

contract Greeter {
    string public greeting;
    
    constructor() {
        greeting = "hello";
    }
    
    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }
    
    function greet() view public returns (string memory) {
        return greeting;
    }
}
