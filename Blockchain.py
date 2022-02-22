from urllib.parse import urlparse
import datetime
import hashlib
import json
import requests

from Block import Block
from Transaction import Transaction


class Blockchain:
    def __init__(self):
        self.chain = []  # 블록들의 리스트 => 블록체인
        self.transaction_list = []
        # 타겟 난이도 비트
        self.bits = 2
        self.nodes = set()

        genesis_nonce = self.proof_of_work(100)
        genesis_block = Block(None, [], datetime.datetime.now(), self.bits, genesis_nonce)
        genesis_block.generate_hash()
        self.chain.append(json.loads(str(genesis_block)))

    def make_transaction(self, amount, receiver_address, sender_address, sender_private_key):
        transaction = Transaction(self, amount, receiver_address, sender_address, sender_private_key)
        # try:
        #     transaction = Transaction(self, amount, receiver_address, sender_address, sender_private_key)
        # except Exception as e:
        #     return str(e)
        self.transaction_list.append(json.loads(str(transaction)))
        return transaction.hash

    def create_block(self, miner_address):
        nonce = self.proof_of_work(self.get_previous_block()['nonce'])
        tx_list = self.transaction_list
        # 코인 베이스 트랜잭션
        tx_list.insert(0, json.loads(str(Transaction(self, 20, miner_address))))
        self.transaction_list = []
        last_block = self.chain[-1]
        new_block = Block(last_block['hash'], tx_list, datetime.datetime.now(), self.bits, nonce)
        new_block.generate_hash()
        self.chain.append(json.loads(str(new_block)))
        return json.loads(str(new_block))

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
            # 블록의 해쉬값 확인
            if block['previous_block'] != last_block['hash']:
                return False
            last_block = block
            current_index += 1
        return True
