from web3 import Web3

def web3_status():
    w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/c22ce0861a6647d8bbd10fd3ebc7970b'))
    web_status = w3.isConnected()
    return web3_status


