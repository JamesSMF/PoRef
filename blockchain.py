import time
from block import Block
from math import inf
from collections import defaultdict

class PoW_Blockchain:
    def __init__(self, difficulty):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty = difficulty

    def create_genesis_block(self):
        # Initialize the head of the blockchain
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block, diff = None):
        if not diff:
            diff = self.difficulty
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * diff):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash()

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, unconfirmed_transactions, difficulty = None):
        if not difficulty:
            difficulty = self.difficulty
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block, difficulty)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block

class PoRef_Blockchain(PoW_Blockchain):
    def __init__(self, difficulty, users, time_limit = 3):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty = difficulty
        self.users = users

    def assign_id(self):
        time_list = []
        self.unconfirmed_transactions = [{}] * len(self.users)
        for u in self.users:
            start = time.time()
            self.mine(self.unconfirmed_transactions, 2)
            end = time.time()
            time_list.append((end - start, u))

        time_list.sort(key = lambda x: x[0])
        for rank, (t, u) in enumerate(time_list):
            u.id = rank + 1

        return [i.reputation for i in self.users]


    def proof_of_referral(self, reputation_list, votes):
        N = len(reputation_list)

        # We should pass in structures like this: [(id, reputation), ...]
        def three_sum(supporters):
            for i in range(len(supporters)):
                l, r = i + 1 , len(supporters) - 1
                while l < r:
                    cur_sum = supporters[i][0] + supporters[l][0] + supporters[r][0]
                    if cur_sum == N + 1:
                        return supporters[i][1] + supporters[l][1] + supporters[r][1]
                    else:
                        return -inf

        vote_dict = defaultdict(list)
        for idx, vote in enumerate(votes):
            for i in vote:
                vote_dict[i].append((idx, reputation_list[idx]))

        validator, adv, max_reputation = None, [], -inf
        for user, sp in vote_dict.items():
            if len(sp) > 2:
                cur_reputation = three_sum(sp)
                if cur_reputation > max_reputation:
                    max_reputation = cur_reputation
                    validator = user
                    adv = sp

        return validator, adv

    def validate_block(self, validator, adv):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        # For simplicity, we do the hash calculation here. In reality, the validator will do it
        new_hash = new_block.compute_hash()
        self.add_block(new_block, proof)
        self.unconfirmed_transactions.pop(0)
        validator.validate_succcess()
        for i in adv:
            i.advocate_success()
        return new_block
