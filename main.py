from web3 import Web3
from core import transaction as transaction
from core import blocks as blocks
from core import smart_contracts as smart_contracts
from rich import print
from rich.console import Console
from rich.markdown import Markdown

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
menu = """
####################################################
######### ETH Blockchain operations Script #########
####################################################
1. Show Menu.
2. Show ETH Accounts and their balance.
3. Make a transaction.
4. Block Operations (Will clear Console).
5. List Transactions.
6. Lookup Transactions.
7. Convert Wei to ETH.
8. Convert ETH to Wei.
9. Smart Contracts Operations.
10. Print README.md.

0. Quit.
####################################################
"""
print(menu)
while True:
	print('[bold red]Press 1 to show the Menu, press 0 to quit.[/bold red]')
	index = int(input())
	if index == 0:
		break
	if index == 1:
		print(menu)
	if index == 2:
		transaction.checkBalance(web3)
	if index == 3:
		try:
			transaction.makeTransaction(web3)
		except Exception as e:
			print(f'[yellow]Something unexpected occured in this menu - {e}')
	if index == 4:
		blocks.lookUpBlock(web3)
	# iterate through blockchain blocks and print out the transactions hashes
	if index == 5:
		transaction.list_transactions(web3)
	if index == 6:
		tx_hash = input('Type the hash of the transaction:\n')
		transaction.lookup_transaction(web3, tx_hash)
	if index == 7:
		wei = input('Type value in Wei:\n')
		result = web3.fromWei(int(wei), 'ether')
		print(f'Result:\n{result} ETH')
	if index == 8:
		eth = input('Type value in ETH:\n')
		result = web3.toWei(eth, 'ether')
		print(f'Result:\n{result} Wei')
	# instead os setting up a truffle project and create smart contracts, in this program we will use remix to ilustrate
	if index == 9:
		try:
			smart_contracts.deploy_menu(web3)
		except Exception as e:
			print(f'[yellow]Something unexpected occured in this menu - {e}')
	# use rich library to print the README.md file
	if index == 10:
		console = Console()
		with open('README.md','r') as file:
			data = file.read()
			md = Markdown(data)
			console.print(md)