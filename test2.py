from Mine import *
from Transaction import *
import time
from flask import Flask, jsonify
from flask import request
import requests

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

b = Blockchain()
m = Mine(b)
t = Transaction(b)


@app.route('/', methods=['GET'])
def get_chain():
    response = {
        'chain': b.chain,
        'length': len(b.chain)
    }
    return response


@app.route('/mine', methods=['GET'])
def mining():
    block = m.mining()
    responses = {
        'message': 'Congrate! you mined a block!',
        **block
    }
    return responses


@app.route('/add_transaction', methods=['GET'])
def add_transaction():
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

    print(index)
    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
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
def update_chain():
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
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5001)
