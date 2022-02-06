from urllib.parse import urlparse
import datetime
import hashlib
import json
import requests


class Blockchain:
    def __init__(self):
        self.chain = []  # 블록들의 리스트 => 블록체인
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        # 가장 첫 블록엔 '제네시스블록'을 생성하기 위해 proof를 1, previous_hash를 0으로 한다.
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        # json으로 구조화된 block을 생성하고
        # chain에 append 해준 뒤 block을 리턴한다.
        block = {
            'index': len(self.chain),
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 0
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2
                                                - previous_proof ** 2).encode()).hexdigest()
            # 이전 pow값과의 연산값을? sha256으로 암호화함
            # 0의 개수를 조정해서 난이도 조절
            if hash_operation.startswith('0000'):
                check_proof = True
            # 만약 해당 암호화값이 특정 조건을 만족하는 경우 해당 proof값을 리턴함.
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def update_chain(self):
        longest_chain = None
        max_length = len(self.chain)

        for node in self.nodes:
            response = requests.get(f'http://{node}/')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

    # 딕셔너리 형태의 block을 받아서 json으로 dump하고 인코딩하여 해시값을 얻어 리턴함

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            # print('%s' % last_block)
            # print('%s' % block)
            # print("\n---------\n")
            #블록의 해쉬값 확인
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1
        return True

