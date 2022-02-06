from Blockchain import *

class Transaction(Blockchain):
    def __init__(self, b):
        self.blockchain = b

    def add_transaction(self, sender, receiver, amount):
        block = self.blockchain.get_previous_block()
        block['transactions'].append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        print(self.blockchain.transactions)
        return self.blockchain.get_previous_block()['index'] + 1



