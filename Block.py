import copy
import hashlib
import json


class Block:
    def __init__(self, prev_block, transactions, timestamp, bits, nonce):
        # 블록 헤더
        self.prev_block = prev_block
        self.mercle_root = self.gen_mrkl_root(transactions)
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.hash = None
        # 트랜잭션
        self.transactions = json.dumps(transactions)

    def gen_mrkl_root(self, transactions):
        if len(transactions) == 0:
            return None
        temp = [hashlib.sha256(str(x).encode()).hexdigest() for x in transactions]

        while not len(temp) == 1:
            if len(temp) % 2 == 1:
                temp.append(copy.copy(temp[-1]))
            temp = [hashlib.sha256((str(temp[i]) + str(temp[i + 1])).encode()).hexdigest() for i in
                    range(0, len(temp), 2)]

        return temp[0]

    def generate_hash(self):
        encoded_block = str(self).encode()
        self.hash = hashlib.sha256(encoded_block).hexdigest()

    def __str__(self):
        result = {
            'mercle_root': self.mercle_root,
            'timestamp': str(self.timestamp),
            'bits': self.bits,
            'nonce': self.nonce,
            'hash': self.hash,
            'transactions': self.transactions
        }

        if self.prev_block is not None:
            result['previous_block'] = self.prev_block

        return json.dumps(result, sort_keys=False)

