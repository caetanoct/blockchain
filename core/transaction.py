from web3 import Web3
from decimal import Decimal
from modules.parse import attributedict_to_json
from rich import print_json
from rich import print
# get all transaction receipts and return them as a list
def fetch_all_receipts(web3_rpc_object):
	receipts = []
	latest_block = web3_rpc_object.eth.block_number
	for i in range(latest_block+1):
		transactions_list = web3_rpc_object.eth.get_block(i).transactions
		for transaction in transactions_list:
			tx_hash = transaction.hex()
			receipts.append(web3_rpc_object.eth.get_transaction_receipt(tx_hash))
	return receipts
# print out the transaction receipt of a given tx_hash
def get_transaction_receipt(web3_rpc_object,tx_hash):
	print(attributedict_to_json(dict(web3_rpc_object.eth.get_transaction_receipt(tx_hash))))
# loop through all transactions in all blocks in the blockchain and print them with their destination/source addresses
def list_transactions(web3_rpc_object):
	latest_block = web3_rpc_object.eth.block_number
	for i in range(latest_block+1):
		transactions_list = web3_rpc_object.eth.get_block(i).transactions
		for transaction in transactions_list:
			tx_hash = transaction.hex()			
			to,source = get_to_and_from(web3_rpc_object,transaction)
			print(f'[green bold]{tx_hash}[/green bold]\n\tfrom {source}\n\tto {to}')
# return all information from web3 API return of get_transaction function in JSON format
def lookup_transaction(web3_rpc_object, tx_hash):
	print_json(attributedict_to_json(web3_rpc_object.eth.get_transaction(tx_hash)))
# return the source/destination address of a given transaction
def get_to_and_from(web3_rpc_object, tx_hash):
	tx_attribute_dict = web3_rpc_object.eth.get_transaction(tx_hash)
	return (tx_attribute_dict.to,tx_attribute_dict['from'])	
# loop through all acounts in eth network and list their balances
def checkBalance(web3_rpc_object):
	print("--- These are the accounts listed in the Blockchain and their Balance ---")
	accounts = web3_rpc_object.eth.accounts
	for i,account in enumerate(accounts):
		account_balance = web3_rpc_object.eth.get_balance(account)
		eth_amount = web3_rpc_object.fromWei(account_balance, 'ether')
		print(f'{i} - {account} - {eth_amount} ETH')
# gets sender account, and recipient acount, sender account private key and the value of the transaction
# make the transaction using the minimum amount of gas with de maximum gas price of the network
def makeTransaction(web3_rpc_object):
	print("--- These are the accounts listed in the Blockchain ---")
	accounts = web3_rpc_object.eth.accounts
	for i,account in enumerate(accounts):
		print(f'{i} - {account}')
	index = int(input("Type the index of the sender account.\n"))
	sender_account = accounts[index]
	index = int(input("Type the index of the recipient account.\n"))
	recipient_account = accounts[index]
	private_key = input("Paste sender private key in order to sign the transaction.\n")
	# balance in wei
	sender_account_balance = web3_rpc_object.eth.get_balance(sender_account)
	eth_amount = input(f"Type the amount of ETH you want to send. Sender balance is {web3_rpc_object.fromWei(sender_account_balance, 'ether')} ETH.\n")
	eth_amount_wei = web3_rpc_object.toWei(eth_amount, 'ether')
	if eth_amount_wei > sender_account_balance:
		print("The sender can't make this transaction, the balance is not enough.")
	else:
		# prevents a transaction from being made twice on Ethereum
		nonce = web3_rpc_object.eth.getTransactionCount(sender_account)
		tx = {
			'nonce' : nonce,
			'to' : recipient_account,
			'value' : eth_amount_wei,
			# maximum gas price
			'gasPrice' : 2000000000,
			# minimum amount of gas
			'gas' : 21000
		}
		# signing transaction
		# Returns a transaction that’s been signed by the node’s private key, but not yet submitted. The signed tx can be submitted with Eth.send_raw_transaction
		signed_tx = web3_rpc_object.eth.account.signTransaction(tx,private_key)
		# send the raw transaction and get the transaction hash
		tx_hash = web3_rpc_object.eth.send_raw_transaction(signed_tx.rawTransaction)
		print('Waiting for transaction receipt.')
		web3_rpc_object.eth.waitForTransactionReceipt(tx_hash)
		print('-- Transaction Result --')		
		print_json(attributedict_to_json(web3_rpc_object.eth.get_transaction(tx_hash)))
if __name__ == '__main__':
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
	ganache_url = "http://127.0.0.1:8545"
	web3 = Web3(Web3.HTTPProvider(ganache_url))
	list_transactions(web3)