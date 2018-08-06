import json
import time
import ethereum
import web3
from flask import Flask, request
from flask_restful import Resource, Api, abort

from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider("http://127.0.0.1:7545"))

w3.eth.enable_unaudited_features()


app = Flask(__name__)
api = Api(app)


Abi="""[ { "constant": false, "inputs": [ { "name": "_procedureId", "type": "uint256" }, { "name": "_priceInTokens", "type": "uint256" } ], "name": "changeProcedurePrice", "outputs": [ { "name": "_procedurePriceChanged", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "whiteListAnyProvider", "outputs": [ { "name": "_whiteListed", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "viewAllProviders", "outputs": [ { "name": "", "type": "address[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_blocknumber", "type": "uint256" }, { "name": "_procedureId", "type": "uint256" } ], "name": "checkProcedurePriceByBlock", "outputs": [ { "name": "_procedurePriceAtBlokcnumber", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "providers", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_procedureId", "type": "uint256" } ], "name": "approveProcedureListing", "outputs": [ { "name": "_procedureApproved", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "applyForWhiteListing", "outputs": [ { "name": "_applied", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "contractOwner", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_procedureId", "type": "uint256" }, { "name": "_priceInTokens", "type": "uint256" } ], "name": "listProcedure", "outputs": [ { "name": "_procedureListed", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "viewProcedures", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "checkIfProviderExists", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_procedureId", "type": "uint256" } ], "name": "checkCurrentProcedurePrice", "outputs": [ { "name": "_procedurePrice", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" } ], "name": "appliedForWhitelisting", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" } ], "name": "whiteListed", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" } ], "name": "procedureListedSuccess", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" } ], "name": "procedureApproved", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" }, { "indexed": true, "name": "_priceChangedTo", "type": "uint256" } ], "name": "procedurePriceChanged", "type": "event" } ]"""

#Enter your deployed contract address here
contract_address= Web3.toChecksumAddress("0x46a4e325f2aa8af41b9b7f2b2ebf744408610a4a")
contract = w3.eth.contract(address = contract_address, abi =Abi)




class applyForWhiteListing(Resource):
    def post(self):
        address=request.json["address"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.applyForWhiteListing(address).buildTransaction({
            'chainId': 5777,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):

            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)
        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.appliedForWhitelisting().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Applied":"Success"}


class whiteListAnyProvider(Resource):
    def post(self):
        address=request.json["address"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.whiteListAnyProvider(address).buildTransaction({
            'chainId': 5777,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):

            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)
        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.whiteListed().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Whitelisting":"Success"}

class approveProcedureListing(Resource):
    def post(self):
        address=request.json["address"]
        procedure_id=request.json["procedure_id"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.approveProcedureListing(address,procedure_id).buildTransaction({
            'chainId': 5777,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):

            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)
        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.procedureApproved().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Procedure_approved":"Success"}


class listProcedure(Resource):
    def post(self):
        price=request.json["price"]
        procedure_id=request.json["procedure_id"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.listProcedure(procedure_id,price).buildTransaction({
            'chainId': 5777,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):

            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)
        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.procedureListedSuccess().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Procedure_listed":"Success"}


class changeProcedurePrice(Resource):
    def post(self):
        price=request.json["price"]
        procedure_id=request.json["procedure_id"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.changeProcedurePrice(procedure_id,price).buildTransaction({
            'chainId': 5777,
            'gas': 140000,
            'gasPrice': w3.toWei('40', 'gwei'),
            'nonce': nonce,
        })

        signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_receipt = w3.eth.getTransactionReceipt(result)

        count = 0
        while tx_receipt is None and (count < 30):

            time.sleep(10)

            tx_receipt = w3.eth.getTransactionReceipt(result)
        if tx_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        processed_receipt = contract.events.procedurePriceChanged().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Procedure_Price_Changed":"Success"}




class checkCurrentProcedurePrice(Resource):
    def post(self):
        address=request.json["address"]
        procedure_id=request.json["procedure_id"]
        return {"Procedure_price":contract.functions.checkCurrentProcedurePrice(address,procedure_id).call()}

class viewProcedures(Resource):
    def post(self):
        address=request.json["address"]
        return {"Procedures_for_address":contract.functions.viewProcedures(address).call()}



class checkProcedurePriceByBlock(Resource):
    def post(self):
        address=request.json["address"]
        procedure_id=request.json["procedure_id"]
        blocknumber=request.json["blocknumber"]
        return {"Procedures_for_address":contract.functions.checkProcedurePriceByBlock(address,blocknumber,procedure_id).call()}


class checkIfProviderExists(Resource):
    def post(self):
        address=request.json["address"]
        return {"Procedures_for_address":contract.functions.checkIfProviderExists(address).call()}




api.add_resource(applyForWhiteListing, '/v1/applyForWhiteListing')
api.add_resource(checkIfProviderExists, '/v1/checkIfProviderExists')
api.add_resource(checkProcedurePriceByBlock, '/v1/checkProcedurePriceByBlock')
api.add_resource(viewProcedures, '/v1/viewProcedures')
api.add_resource(checkCurrentProcedurePrice,'/v1/checkCurrentProcedurePrice')
api.add_resource(changeProcedurePrice,'/v1/changeProcedurePrice')
api.add_resource(listProcedure, '/v1/listProcedure')
api.add_resource(whiteListAnyProvider,'/v1/whiteListAnyProvider')
api.add_resource(approveProcedureListing,'/v1/approveProcedureListing')




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)