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
app.config.from_object('config')
api = Api(app)


Abi="""[ { "constant": false, "inputs": [ { "name": "_procedureId", "type": "uint256" }, { "name": "_priceInTokens", "type": "uint256" } ], "name": "changeProcedurePrice", "outputs": [ { "name": "_procedurePriceChanged", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "whiteListAnyProvider", "outputs": [ { "name": "_whiteListed", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "viewAllProviders", "outputs": [ { "name": "", "type": "address[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_blocknumber", "type": "uint256" }, { "name": "_procedureId", "type": "uint256" } ], "name": "checkProcedurePriceByBlock", "outputs": [ { "name": "_procedurePriceAtBlokcnumber", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "", "type": "uint256" } ], "name": "providers", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_procedureId", "type": "uint256" } ], "name": "approveProcedureListing", "outputs": [ { "name": "_procedureApproved", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "applyForWhiteListing", "outputs": [ { "name": "_applied", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "contractOwner", "outputs": [ { "name": "", "type": "address" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": false, "inputs": [ { "name": "_procedureId", "type": "uint256" }, { "name": "_priceInTokens", "type": "uint256" } ], "name": "listProcedure", "outputs": [ { "name": "_procedureListed", "type": "bool" } ], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "viewProcedures", "outputs": [ { "name": "", "type": "uint256[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" } ], "name": "checkIfProviderExists", "outputs": [ { "name": "", "type": "bool" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [ { "name": "_provider", "type": "address" }, { "name": "_procedureId", "type": "uint256" } ], "name": "checkCurrentProcedurePrice", "outputs": [ { "name": "_procedurePrice", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "inputs": [], "payable": false, "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" } ], "name": "appliedForWhitelisting", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" } ], "name": "whiteListed", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" } ], "name": "procedureListedSuccess", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" } ], "name": "procedureApproved", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "name": "_provider", "type": "address" }, { "indexed": true, "name": "_procedureId", "type": "uint256" }, { "indexed": true, "name": "_priceChangedTo", "type": "uint256" } ], "name": "procedurePriceChanged", "type": "event" } ]"""

#Enter your deployed contract address here
contract_address= Web3.toChecksumAddress("0x50581466489d04dcb1dfe4f1d35307b004ee306f")
contract = w3.eth.contract(address = contract_address, abi =Abi)




class registercar(Resource):
    def post(self):
        address=request.json["address"]
        vin_number=request.json["vinnumber"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.register(address,vin_number).buildTransaction({
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

        processed_receipt = contract.events.Registered().processReceipt(tx_receipt)

        if processed_receipt:
            return {"Registration_status":"Success","vin_number":vin_number}

                
class ownedcars(Resource):
    def post(self):
        address=request.json["address"]
        return {"owned_cars":contract.functions.ownedCars(address).call()}



class carprice(Resource):
    def post(self):
        vin_number=request.json["vinnumber"]
        return {"Car_price":contract.functions.price(vin_number).call()}


class listcar(Resource):
    def post(self):
        value=request.json["value"]
        vin_number=request.json["vinnumber"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = contract.functions.list(vin_number,value).buildTransaction({
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

        processed_receipt = contract.events.Listed().processReceipt(tx_receipt)

        if processed_receipt:
            return {"car_listed":"success"}

#get tokens by sending some ether to contract address       
class getTokens(Resource):
    def post(self):
        amount_in_ether=request.json["ether"]
        contractAddress=request.json["contractAddress"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        amount_in_wei = amount_in_ether * 1000000000000000000;

        nonce = w3.eth.getTransactionCount(wallet_address)

        txn_dict = {
                'to': contractAddress,
                'value': amount_in_wei,
                'gas': 2000000,
                'gasPrice': w3.toWei('40', 'gwei'),
                'nonce': nonce,
                'chainId': 5777
        }

        signed_txn = w3.eth.account.signTransaction(txn_dict, wallet_private_key)
        
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        txn_receipt = None

        count = 0
        while txn_receipt is None and (count < 30):

            txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

            

            time.sleep(10)


        if txn_receipt is None:
            return {'status': 'failed', 'error': 'timeout'}

        return {'status': 'Success'}


class buycar(Resource):
    def post(self):
        value=request.json["value"]
        vin_number=request.json["vinnumber"]
        wallet_address=request.json["wallet_address"]
        wallet_private_key=request.json["Private_key"]
        nonce = w3.eth.getTransactionCount(wallet_address)
        txn_dict = contract.functions.buyCar(vin_number,value).buildTransaction({
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

        return {'status': 'Success'}

api.add_resource(registercar, '/v1/registercar')
api.add_resource(ownedcars, '/v1/ownedcars')
api.add_resource(listcar, '/v1/listcar')
api.add_resource(carprice, '/v1/carprice')
api.add_resource(buycar,'/v1/buycar')
api.add_resource(getTokens,'/v1/buytokens')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)