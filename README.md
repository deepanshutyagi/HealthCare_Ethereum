Compile and deploy contract;
```
Run Truffle compile
Run Truffle migrate after editing ur ganache infot in truffle.js
Interact with the contract
There is a python backend restapi implementation in app folder,file is called interact.py
```

Install python3 and pip
```
brew install python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```


Create a virtual envrionment in python  
```
python3 -m pip install --user virtualenv
python3 -m virtualenv env
source env/bin/activate
```
Install the required packages
```
cd ./app
pip install -r requirements.txt
```
Run app and interact with the smart contract
```
change the contract address in interact.py script
Your ganache url
w3 = Web3(HTTPProvider("your url"))
contract_address= Web3.toChecksumAddress("your address")
cd ./app
Run python3 interact.py
Interact with smart contract using the post endpoints in the postman folder
```


