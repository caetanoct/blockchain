from web3 import Web3
import pprint
import os
clear = lambda: os.system('clear')
def lookUpBlock(web3_rpc_object):
	latest_block = web3_rpc_object.eth.block_number
	clear()
	print(f"""
### Select Block Operation ###
Press 0 to Iterate Through all blocks and show their information.
Or press the number of the block you want to lookup.
		""")
	blockchain_string = ""
	for i in range(latest_block+1):
		if i == latest_block:
			blockchain_string = blockchain_string + str(i)
		else:
			blockchain_string = blockchain_string + str(i) + " -> "
	print(blockchain_string)
	index = int(input('Type 0 or the index of the block:\n'))
	if index == 0:
		for i in range(latest_block+1):
			print(f'#### BLOCK {i} ####')
			dictionary = dict(web3_rpc_object.eth.get_block(i))
			pprint.pprint(dictionary)
			print(f'#### END OF BLOCK {i} ####')
	else:
		if index <= latest_block:
			dictionary = dict(web3_rpc_object.eth.get_block(index))
			pprint.pprint(dictionary)
		else:
			print('This block number is too large.')