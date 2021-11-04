import json
from web3 import Web3
if __name__ != '__main__':
	from modules.parse import attributedict_to_json
	from core.transaction import fetch_all_receipts
from rich import print_json
from rich import print

# global variable that contains all the available contract adresses
available_contracts_list = []
# global list that contains the contracts that were instatiated with ABI
contracts_list = []
# retrieve all available contract addresses in the blockchain
def fetch_blockchain_contract_addresses(web3):
	addresses = set()
	receipts = fetch_all_receipts(web3)
	for receipt in receipts:
		if receipt.contractAddress != None:
			addresses.add(receipt.contractAddress)
	return list(addresses)
# given a contract print out its given ABI in JSON format and check wether the functions take input or not
def print_contract_abi_names(contract):
	print('--- Contract Names/Functions ---')
	for i in contract.abi:
		if 'name' in i:
			name = i['name']
			if len(i['inputs']) > 0:
				print(f'{name} - Takes Input')
			else:
				print(f'{name} - Does not take Input')			
# print the contract ABI in JSON format
def print_contract_abi(contract):
	print('--- Contract ABI ---')
	print_json(data=contract.abi)
# show all contracts in blockchain and if they we have the ABI stored on the program data or not
def print_contract_list():	
	print('--- Contract List (index - address) ---')
	for i,contract in enumerate(available_contracts_list):
		contract_has_abi = False
		for contract_obj in contracts_list:
			if contract == contract_obj.address:
				contract_has_abi = True
		if contract_has_abi:
			print(f'{i} - {contract}')
		else:
			print(f'{i} - {contract} - [bold red] missing ABI [/bold red]')
	print('---------------------------------------')
# select a contract from the list and return the contract obj
def select_contract():
	print_contract_list()
	i = int(input('Select contract by index.\n'))
	if i < len(available_contracts_list):
		address = available_contracts_list[i]
	else:
		print('Invalid index.')
	for contract_obj in contracts_list:
		if address == contract_obj.address:
			return contract_obj
# deploy the Smart Contracts operations Menu	
def deploy_menu(web3):
	menu = """
###################################################
######### ETH Blockchain Contracts Script #########
###################################################
1. Show Menu.
2. Add a Existing Contract to the List
3. Compile and Deploy a Contract
4. Print Contracts List
5. Select and Print Contract ABI
6. Select and Print Contract ABI names
7. Call greet()
8. Call setGreeting()

0. Quit.
###################################################
	"""
	print(menu)
	while True:	
		# refresh abailable contract list
		global available_contracts_list
		available_contracts_list = fetch_blockchain_contract_addresses(web3)
		print('[bold green]Press 1 to show the Menu, press 0 to quit this contract menu and return to main menu.[/bold green]')
		index = int(input())
		if index == 0:
			break
		if index == 1:
			print(menu)
		if index == 2:
			print_contract_list()
			addr = input("Paste the contract address.\n")
			abi = json.loads(input("Paste the 1 line ABI.\n"))
			# format to checksum addres (ganache and remix uses it)
			ctract_addr = web3.toChecksumAddress(addr)
			#contract = web3.eth.contract(address=ctract_addr,abi=abi)
			contract = web3.eth.contract(address=ctract_addr,abi=abi)
			contracts_list.append(contract)
			print(f'Contract added - {contract}')			
			#contract = web3.eth.contract(address=web3.toChecksumAddress("0x6f03A8Fc467c9455DE2D7fC5bbE3DF839db69d61"),abi=json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"greet","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"greeting","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_greeting","type":"string"}],"name":"setGreeting","outputs":[],"stateMutability":"nonpayable","type":"function"}]'))			
		if index == 3:
			path = select_source_code()
			compile_and_deploy_contract(path,web3)
		if index == 4:
			print_contract_list()
		if index == 5:
			contract = select_contract()
			print_contract_abi(contract)
		if index == 6:
			contract = select_contract()
			print_contract_abi_names(contract)
		if index == 7:
			contract = select_contract()
			print(contract.functions.greet().call())
		if index == 8:
			contract = select_contract()
			# using first account from the blockchain to create
			web3.eth.defaultAccount = web3.eth.accounts[0]
			string = input('Type the new greeting \n')
			# the tx_hash is instant but we need to wait for the transaction to be mined and confirmed
			tx_hash = contract.functions.setGreeting(string).transact()
			print('Waiting for transaction receipt.')
			web3.eth.waitForTransactionReceipt(tx_hash)
			print(f'Transaction Result:\n')			
			print_json(attributedict_to_json(web3.eth.get_transaction(tx_hash)))		
# let the user choose which contract he wants to compile and return it's path
def select_source_code():
	# list the sorce codes
	import os
	list_of_contents = os.listdir("./core/contracts")
	print('--- [bold green].sol[/bold green] files in contracts directory ---')
	for i,file in enumerate(list_of_contents):
		print(f'{i} - {file}')
	print('Select contract by index')
	index = int(input())
	selected_contract_path = "./core/contracts/"+list_of_contents[index]
	print(f'Selected contract is: {selected_contract_path}')
	return selected_contract_path
# compile and deploy the contract on the blockchain
def compile_and_deploy_contract(path,web3):
	with open(path,'r') as file:
		sol_source_code = file.read()
		from solcx import compile_source
		compiled_sol = compile_source(sol_source_code)
		# retrieve the contract interface
		contract_id, contract_interface = compiled_sol.popitem()
		# get bytecode / bin
		bytecode = contract_interface['bin']
		# get abi
		abi = contract_interface['abi']
		# set pre-funded account as sender
		web3.eth.default_account = web3.eth.accounts[0]
		Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
		# Submit the transaction that deploys the contract
		tx_hash = Contract.constructor().transact()
		# Wait for the transaction to be mined, and get the transaction receipt
		tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
		print(f'Contract added:\n\tcontract address: {tx_receipt.contractAddress}\n\thash: {tx_hash.hex()}')
		# adds the contract to contract list
		contracts_list.append(web3.eth.contract(address=tx_receipt.contractAddress, abi=abi))
if __name__ == '__main__':
	ganache_url = "http://127.0.0.1:8545"
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	import json
	from hexbytes import HexBytes
	def attributedict_to_json(tx):	
		txdict = dict(tx)
		return json.dumps(txdict, cls=HexJsonEncoder)
	class HexJsonEncoder(json.JSONEncoder):
		def default(self, obj):
			if isinstance(obj, HexBytes):
				return obj.hex()
			return super().default(obj)
	#fetch_blockchain_contract_addresses(web3)
	deploy_menu(web3)