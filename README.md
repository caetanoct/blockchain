# Blockchain Applications Development

### Tools Used
* [Ganache](https://github.com/trufflesuite/ganache) - Ganache offers both desktop and command-line varieties. In this case we tested ganache-cli. Ganache is a quick and easy way to run a personal blockchain for developing and deploying smart contracts.
* [Remix](https://remix.ethereum.org/) - used to manage smart contract, testing, compiling, and deploying.

### Quick Ganache Setup Guide

1. Run
```sh
npm install ganache@alpha --global
```
2. Once installed run
```sh
ganache
```
3. You should get an output like that:
```
bigint: Failed to load bindings, pure JS will be used (try npm run rebuild?)
ganache v7.0.0-alpha.1 (@ganache/cli: 0.1.1-alpha.1, @ganache/core: 0.1.1-alpha.1)
Starting RPC server

Available Accounts
==================
(0) 0x27ECad10f06Ec722E79C2baf51f6064A58390922 (1000 ETH)
(1) 0x896Eeed3899e6638ae6d972FEff5a9D0CdAbd7E2 (1000 ETH)
(2) 0xD03C6Bc5bD22B929F8F7b1d98d2C41d37453a391 (1000 ETH)
(3) 0xD672a7efCC694D01a843385D9F5d133772B1CeDC (1000 ETH)
(4) 0x2328379E61C101bb234A930044c5291101EfC0c0 (1000 ETH)
(5) 0x06f4CefAda05ce555c28990214a3EB0C9FfA4572 (1000 ETH)
(6) 0x3b36596E685d07E39A97e75a4D8eF8e4b7Fdc5AA (1000 ETH)
(7) 0x38647c5837370B2Ef0f76Bf5A531E122095d3C39 (1000 ETH)
(8) 0x583be075055e07C5aFAD3F833dE790acbb185E4D (1000 ETH)
(9) 0xb0BD8d7361635803D2E5179c601B1473bC8D93D2 (1000 ETH)

Private Keys
==================
(0) 0xda6c5b201180706b8fbf37813cc01b76ae3c358c5608e42418644c847d813fce
(1) 0x1c23fd6f99301086febab5cdb8067803b71c9133ca25e2d60d5647cd4cb9c751
(2) 0x1f1828dfd1b276fe9b495d70d70c5cb1ef91c87f9fdf83f9bd2858bc7ef03c40
(3) 0x6612719e9a67febb7ca1b31abe314d7dca9383469701da1b43df3dc3394f5e3c
(4) 0xcd688e3301515ecd3b5f48ec2b79f3834bbf6cc1b213936b5133e00e42575fad
(5) 0x99a215bb86c841f82d727174092aa6658e9c52a7d0028fc42dc59490a52a39f9
(6) 0x8c183ea59fea02df4d8b00839db3678ef41fad13f198e34e2b946532d7d966f7
(7) 0x14f901fda42e536b27ce49fdc451ca12c25a85d4557b383558b5cbe4ee3295fb
(8) 0xbc351489c5a6885e189f86a898c4e4884f199197d15256c90d08eb51ccac52dd
(9) 0xd7270e28c8378fa6eaad42343531adf6f04027fdaf82c5aeeb579885852c6bb2
```
### Smart Contracts

For Smart Contracts, we will use Remix instead of setting up a Truffle project, the website can be acessed inhttps://remix.ethereum.org/. Just go to the website, create a new Contract under the **Contracts Directory** andpaste the following contract, for example:

```sol
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
```
Then go to **Solidity Compiler** tab and Compile
Then go to **Deploy & Run** tab and choose the environment as Web3 Provider and type the provider endpoint, using ganache it will propably be `http://127.0.0.1:8545`. 
Choose the account and deploy the contract, you can verify that the contract was deployed by listing the transactions.

Take note of the contract address and the ABI.

Note: The ganache/blockchain needs to be up and running for this to work.

By deploying a contract you can do operations on the script with it.

### Getting Contract ABI for using in the Script

1. Go to Remix
2. Go to Compiler Tab
3. Select the contract
4. Click Compilation Details to list more information
5. Click WEB3DEPLOY tab.
6. On the first line, there will be an instantiation of a Contract, get only the 1-line array and copy it as the ABI.

Example for this line.
```js
var greeterContract = new web3.eth.Contract([{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]);
```
Extract only this, this is the 1-line ABI:
```
[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]
```

Alternatively, you can just copy the ABI and format it to 1-line before pasting in the terminal.

### ETH Blocks

The blockchain is made of transactions, they are like records. All the transactions are grouped into blocks that are chained together, each block has it's own number.

The application can be used on the real ethereum blockchain instead of the private ganache development network, but it's not recommended.

### Python Requirements

For running the program you need:
```sh
pip3 install web3
pip3 install rich
```
To be able to compile .sol and deploy contracts without using Remix you need to install:
```sh
pip3 install -U "web3[tester]"
pip3 install py-solc-x
```
after `py-solc-x` is installed we need to install a version of `solc` in the python interpreter:
1. Type `python3`.
2. On the python interpreter type:
```py
from solcx import install_solc
install_solc(version='latest')
```

### Contracts in directory core/contracts

In this directory, we can find a bunch of smart contracts that can be compiled and deployed on the Blockchain by the script. Most of them were extracted from this [website](https://solidity-by-example.org/).

### Gas

How much ether do you need to pay for a transaction?
You pay gas spent * gas price amount of ether, where
* gas is a unit of computation
* gas spent is the total amount of gas used in a transaction
* gas price is how much ether you are willing to pay per gas

Transactions with higher gas price have higher priority to be included in a block.
Unspent gas will be refunded.

Gas Limit
There are 2 upper bounds to the amount of gas you can spend
* gas limit (max amount of gas you're willing to use for your transaction, set by you)
* block gas limit (max amount of gas allowed in a block, set by the network)

### Documentation Links

[web3](https://web3py.readthedocs.io/)
[rich](https://rich.readthedocs.io/)
[solidity-by-example](https://solidity-by-example.org/)
[ERC20](https://solidity-by-example.org/app/erc20/)