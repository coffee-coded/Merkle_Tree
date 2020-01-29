import hashlib
import json
from collections import OrderedDict


class MerkleTree:
    def __init__(self, transactions=None):
        self.transaction = transactions
        self.pastTransaction = OrderedDict()

    def create_tree(self):
        current_right_hash = None
        transactions = self.transaction
        prev_transactions = self.pastTransaction
        temp_transaction = []

        for index in range(0, len(transactions), 2):

            current = transactions[index]

            if index + 1 != len(transactions):
                current_right = transactions[index + 1]

            else:
                current_right = ''

            current_hash = hashlib.sha256(current.encode())

            if current_right != '':
                current_right_hash = hashlib.sha256(current_right.encode())

            prev_transactions[transactions[index]] = current_hash.hexdigest()

            if current_right != '':
                prev_transactions[transactions[index + 1]] = current_right_hash.hexdigest()

            if current_right != '':
                temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())

            else:
                temp_transaction.append(current_hash.hexdigest())

        if len(transactions) != 1:
            self.transaction = temp_transaction
            self.pastTransaction = prev_transactions

            self.create_tree()

    def get_past_transaction(self):
        return self.pastTransaction

    def get_root(self):
        last_key = list(self.pastTransaction.keys())[-1]
        return self.pastTransaction[last_key]


if __name__ == "__main__":
    tree = MerkleTree()

    tree.transaction = ['a', 'b', 'c', 'd']

    tree.create_tree()

    past_transaction = tree.get_past_transaction()

    print("First Example - Even number of transaction Merkle Tree")
    print('Final root of the tree : ', tree.get_root())
    print(json.dumps(past_transaction, indent=4))
    print("-" * 50)

    print("Second Example - Odd number of transaction Merkle Tree")
    tree = MerkleTree()
    tree.transaction = ['a', 'b', 'c', 'd', 'e']
    tree.create_tree()
    past_transaction = tree.get_past_transaction()
    print('Final root of the tree : ', tree.get_root())
    print(json.dumps(past_transaction, indent=4))
    print("-" * 50)

    print("Final Example - Actual use case of the Merkle Tree")

    ground_truth_Tree = MerkleTree()
    ground_truth_transaction = ['a', 'b', 'c', 'd', 'e']
    ground_truth_Tree.transaction = ground_truth_transaction
    ground_truth_Tree.create_tree()
    ground_truth_past_transaction = ground_truth_Tree.get_past_transaction()
    ground_truth_root = ground_truth_Tree.get_root()

    tampered_Tree = MerkleTree()
    tampered_Tree_transaction = ['a', 'b', 'c', 'd', 'f']
    tampered_Tree.transaction = tampered_Tree_transaction
    tampered_Tree.create_tree()
    tampered_Tree_past_transaction = tampered_Tree.get_past_transaction()
    tampered_Tree_root = tampered_Tree.get_root()

    print('Company A - my final transaction hash : ', ground_truth_root)
    print('Company B - my final transaction hash : ', ground_truth_root)
    print('Company C - my final transaction hash : ', tampered_Tree_root)

    print("\n\nGround Truth past Transaction ")
    print(json.dumps(ground_truth_past_transaction, indent=4))

    print("\n\nTamper Truth past Transaction ")
    print(json.dumps(tampered_Tree_past_transaction, indent=4))
