from web3 import Web3
import json

# connecting to ganache again
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

with open("abi.json", "r") as f:
    contract_abi = json.load(f)

contract_address = "0x8d4a390246049daA3a5D0a670C42f173e4f89864"

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

account = web3.eth.accounts[1]

tx_hash = contract.functions.authorizeUser(account).transact({'from': web3.eth.accounts[0]})
web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"User {account} authorized!")

# trying to msend a message
receiver = web3.eth.accounts[2]
tx_hash = contract.functions.sendMessage(receiver, "Hello doctor Kim").transact({'from': account})
web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"message sent to {receiver}")

# outputting thee messages
messages = contract.functions.getMessages().call({'from': account})
print("Messages:", messages)
