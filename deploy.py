from web3 import Web3
import json
import solcx
solcx.install_solc('0.8.0')
from solcx import compile_standard, install_solc
install_solc("0.8.0")

with open("Healthcare.sol", "r") as file:
    source_code = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Healthcare.sol": {"content": source_code}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode.object"]
                }
            }
        },
    },
    solc_version="0.8.0",
)


print(compiled_sol)
print(json.dumps(compiled_sol, indent=4))

contract_abi = compiled_sol["contracts"]["Healthcare.sol"]["HealthcareCommunication"]["abi"]
contract_bytecode = compiled_sol["contracts"]["Healthcare.sol"]["HealthcareCommunication"]["bin"]



# Connectting to Ganache, am not sure if it will work
ganache_url = "HTTP://127.0.0.1:7545" # had to change this one a few times
web3 = Web3(Web3.HTTPProvider(ganache_url))
if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache") #trying to check if it will connect, though inakataa
if not web3.is_connected():
    print("Failed to connect to blockchain")
    exit()

with open("abi.json", "r") as f:
    contract_abi = json.load(f)


with open("bytecode.txt", "r") as f:
    contract_bytecode = f.read().strip() # Loadin

deployer_account = web3.eth.accounts[0]

# trying to deploy the contract
HealthcareContract = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
tx_hash = HealthcareContract.constructor().transact({'from': deployer_account, 'gas': 6000000})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# getting the contract address, wueh
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at: {contract_address}")
