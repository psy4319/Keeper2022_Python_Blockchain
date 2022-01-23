
from Blockchain import *

class Transaction(Blockchain):
    def __init__(self):
        Blockchain.__init__(self)
        b = Blockchain()

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.get_previous_block()['index'] + 1



