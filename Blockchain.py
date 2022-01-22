import datetime
import hashlib
import json


class Blockchain:

    def __init__(self):
        self.chain = []  # 블록들의 리스트 => 블록체인
        self.create_block(proof=1, previous_hash='0')
    # 가장 첫 블록엔 '제네시스블록'을 생성하기 위해 proof를 1, previous_hash를 0으로 한다.

    def create_block(self, proof, previous_hash):
        # json으로 구조화된 block을 생성하고
        # chain에 append 해준 뒤 block을 리턴한다.
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]


    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2
                                                - previous_proof ** 2).encode()).hexdigest()
            # 이전 pow값과의 연산값을? sha256으로 암호화함
            if hash_operation.startswith('0000'):
                check_proof = True
            # 만약 해당 암화값이 특정 조건을 만족하는 경우 해당 proof값을 리턴함.
            else:
                new_proof += 1

        return new_proof


    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    # 딕셔너리 형태의 block을 받아서 json으로 dump하고 인코딩하여 해시값을 얻어 리턴함

    def printChain(self,i):
        print(self.chain[i])