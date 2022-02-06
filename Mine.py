from Blockchain import *


class Mine(Blockchain):
    def __init__(self, b):
        self.blockchain = b

    def mining(self):
        blockchain = self.blockchain
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        # print(blockchain.chain)
        return block
