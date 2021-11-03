import json
from web3 import Web3
import pprint
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
contracts_list = []
def print_contract_abi_names(contract):
	print('--- Contract Names/Functions ---')
	for i in contract.abi:
		if 'name' in i:
			name = i['name']
			if len(i['inputs']) > 0:
				print(f'{name} - Takes Input')
			else:
				print(f'{name} - Does not take Input')			
def print_contract_abi(contract):	
	print('--- Contract ABI ---')
	pprint.pprint(contract.abi)
def print_contract_list():
	print('--- Contract List (index - address) ---')
	for i,contract in enumerate(contracts_list):
		print(f'{i} - {contract.address}')
	print('---------------------------------------')
def select_contract():
	print_contract_list()
	i = int(input('Select contract by index.\n'))
	if i < len(contracts_list):
		return contracts_list[i]
	else:
		print('Invalid index.')
def deploy_menu(web3):
	menu = """
###################################################
######### ETH Blockchain Contracts Script #########
###################################################
1. Show Menu.
2. Add a Existing Contract to the List
3. Print Contracts List
4. Select and Print Contract ABI
5. Select and Print Contract ABI names
6. Call greet()
7. Call setGreeting()

0. Quit.
###################################################
	"""
	print(menu)
	while True:	
		index = int(input('Press 1 to show the Menu, press 0 to quit this contract menu and return to main menu.\n'))
		if index == 0:
			break
		if index == 1:
			print(menu)
		if index == 2:			
			abi = json.loads(input("Paste the 1 line ABI.\n"))
			addr = input("Paste the contract address.\n")
			# format to checksum addres (ganache and remix uses it)
			ctract_addr = web3.toChecksumAddress(addr)
			#contract = web3.eth.contract(address=ctract_addr,abi=abi)
			contract = web3.eth.contract(address=ctract_addr,abi=abi)
			contracts_list.append(contract)
			print(f'Contract added - {contract}')			
			#contract = web3.eth.contract(address=web3.toChecksumAddress("0x6f03A8Fc467c9455DE2D7fC5bbE3DF839db69d61"),abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]'))			
		if index == 3:
			print_contract_list()
		if index == 4:
			contract = select_contract()
			print_contract_abi(contract)
		if index == 5:
			contract = select_contract()
			print_contract_abi_names(contract)
		if index == 6:
			contract = select_contract()
			print(contract.functions.greet().call())
		if index == 7:
			contract = select_contract()
			web3.eth.defaultAccount = web3.eth.accounts[0]
			string = input('Type the new greeting \n')
			# the tx_hash is instant but we need to wait for the transaction to be mined and confirmed
			tx_hash = contract.functions.setGreeting(string).transact()
			print('Waiting for transaction receipt.')
			web3.eth.waitForTransactionReceipt(tx_hash)
			print(f'Transaction Result:\n')
			dictionary = dict(web3.eth.get_transaction(tx_hash))
			pprint.pprint(dictionary)