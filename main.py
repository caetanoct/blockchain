from web3 import Web3
import transaction
import blocks
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
menu = """
####################################################
######### ETH Blockchain operations Script #########
####################################################
1. Show Menu.
2. Show ETH Accounts and their balance.
3. Make a transaction.
4. Block Operations.

0. Quit.
####################################################
"""
print(menu)
while True:	
	index = int(input('Press 1 to show the Menu, press 0 to quit.\n'))
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
			print(e)
	if index == 4:
		blocks.lookUpBlock(web3)
	if index == 5:
		pass