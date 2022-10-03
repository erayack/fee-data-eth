import block_maker
import json

def get_percentiles(target_percentiles, block):
    target_percentiles.sort()
    block_gas = sum(block['gas'])
    perc_as_gas =  []
    for index, percentile in enumerate(target_percentiles):
        perc_as_gas.append(percentile * (block_gas // 100))
    txs = []
    for index in range(len(block['fee'])):
        pair = (block['fee'][index], block['gas'][index])
        txs.append(pair)
    txs.sort(key=lambda pair: pair[0])
    cumulative_gas = 0
    tx_index = 0
    percentiles = []
    ongoing = True
    # Go through each gas percentile
    for _, gas_val in enumerate(perc_as_gas):
        # Add transactions, one by one.

        txgas = txs[tx_index][1]
        cumulative_gas += txgas
        # if gas for percentile of interest is less below total gas
        if gas_val < cumulative_gas:
            # Record the fee for the current transaction
            txfee = txs[tx_index][0]
            percentiles.append(txfee)
        # If the tx was large, there may be another fee %ile matched.
        # In which case, continue to next percentile target fee.
        else:
            # The percentile gas is too high relative to tally.
            # While tally low, add transactions to the tally
            while gas_val > cumulative_gas:
                # Increment tx
                tx_index += 1
                txgas = txs[tx_index][1]
                cumulative_gas += txgas
            # When the transactions reach the desired gas percentile
            # Record its fee
            txfee = txs[tx_index][0]
            percentiles.append(txfee)
    # Once percentiles are sorted, add on the highest fee
    percentiles.append(txs[-1][0])
    return percentiles


def get_multiblock_stats(target_percentiles = None, blocks = 2, transactions = 10):
    block_data = block_maker.generate_blocks(
        blocks=blocks, transactions=transactions, save=False)
    if target_percentiles == None:
        target_percentiles = [i*10 for i in range(10)]



    block_stats = []
    for block in block_data['blocks']:
        stats = block
        stats['percentile_response'] = get_percentiles(target_percentiles, block)
        target_percentiles.append(100)
        stats['target_percentiles'] = target_percentiles
        block_stats.append(stats)

    return {'blocks': block_stats}


if __name__ == "__main__":
    data = get_multiblock_stats(
        target_percentiles=None, blocks= 5, transactions = 30
    )

    with open('block_stats.json', 'w') as fp:
        json.dump(data, fp, sort_keys=True)