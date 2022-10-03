import json
import random

def generate_txs(num):
    # {gas: blockgas, fee: maxPriorityGasFee}
    fee_list = []
    gas_list = []
    for i in range(num):
        gas = random.randrange(30000,150000)
        if i % 30 == 0:
            # Every 10th tx may have larger gas up to 1.5million
            gas = random.randrange(30000,1500000)
        gas_list.append(gas)
        fee_list.append(random.randrange(2,100))

    return {'gas': gas_list, 'fee': fee_list}

def generate_blocks(blocks, transactions, save = False):
    # [block]
    block_list = []
    for i in range(blocks):
        block_list.append(generate_txs(transactions))
    data = {'blocks':block_list}
    if save:
        save_data(data)
    return data

def save_data(data):
    with open('blocks.json', 'w') as fp:
        data = generate_blocks(2,5)
        json.dump(data, fp, sort_keys=True)

if __name__ == "__main__":
    data = save_data(2, 30, save = True)