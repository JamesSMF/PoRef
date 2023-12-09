from flask import Flask, request, jsonify
from blockchain import PoW_Blockchain, PoRef_Blockchain
from user import User
from random import randint
from math import inf
from tqdm import tqdm
import requests, json, time

difficulty = 5

app = Flask(__name__)

pow_time = 0
poW = PoW_Blockchain(difficulty)

for _ in range(3):
    min_time = inf
    for _ in tqdm(range(100)):
        start = time.time()
        poW.add_new_transaction({"from": "Alice", "to": "Bob", "amount": 10000})
        poW.mine(poW.unconfirmed_transactions)
        end = time.time()
        if end - start < min_time:
            min_time = end - start

    pow_time += min_time

print('PoW time:', pow_time)


##############################################
##############################################
# Testing PoRef

# First, we generate some dummy users
user_list = []
for _ in range(100):
    user_list.append(User(-1))

# Then, we generate some random votes
votes = []
for _ in range(100):
    votes.append([randint(0, 99) for _ in range(3)])

# Now we can start to test
poref = PoRef_Blockchain(difficulty - 3, user_list)
start = time.time()
for _ in range(3):
    reputation = poref.assign_id()
    validator, adv = poref.proof_of_referral(reputation, votes)
    poref.validate_block(validator, adv)
end = time.time()
print('PoRef time:', end - start)


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in poW.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data),
                    "chain": chain_data})

def main():
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
