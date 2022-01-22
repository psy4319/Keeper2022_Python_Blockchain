from Mine import *
import time
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route('/', methods = ['GET'])
def main():
    m = Mine()
    b = Blockchain()
    i = 0
    #while True:
    mined = mining(m)
    chain = get_chain(b)
        #b.printChain(i) #out of index오류 -> ??
        #i += 1
    time.sleep(1)
    return jsonify(mined , chain), 200


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


app.run(host = '0.0.0.0', port = 5000)

#main()