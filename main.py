from Mine import *
from Transaction import *
import time
from flask import Flask, jsonify
from flask import request
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/', methods = ['GET'])
def main():
    m = Mine()
    b = Blockchain()
    t = Transaction()
    i = 0
    #while True:
    mined = mining(m)
    chain = get_chain(b)
    is_updated = update_chain(b)
    #add_transaction(b)
    #connect_node(b)
#b.printChain(i) #out of index오류 -> ??
    #i += 1
    #time.sleep(1)
    return jsonify(mined, chain, is_updated), 200


def mining(m):
    block = m.mining()
    responses = {
        'message': 'Congrate! you mined a block!',
        **block
    }
    return responses

def get_chain(b):
    response = {
        'chain': b.chain,
        'length': len(b.chain)
    }
    return response

@app.route('/add_transaction', methods=['GET'])
def add_transaction():
    t = Transaction()
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = t.add_transaction(
        sender=json['sender'],
        receiver=json['receiver'],
        amount=json['amount']
    )
    response = {
        'message': f'This transaction will be added to Block {index}'
    }
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node(b):
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        b.add_node(node)
    response = {
        'message': 'All the nodes are now connected. The Hatcoin Blockchain now contains the nodes',
        'total_message': list(b.nodes)
    }
    return jsonify(response), 201


@app.route('/update_chain', methods=['GET'])
def update_chain(b):
    is_chain_updated = b.update_chain()
    if is_chain_updated:
        response = {
            'message': 'The nodes had different chains so the chain was replacted by the longest chain.',
            'new_chain': b.chain
        }
    else:
        response = {
            'message': 'All good. The chain is the largest one.',
            'actual_chain': b.chain
        }
    return response

app.run(host = '0.0.0.0', port = 5000)

#main()