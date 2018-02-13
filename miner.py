
from Queue import Empty
import blockchain
import copy
import custom
import tools
import networking
import multiprocessing
import random
import time
import copy
import target
def make_mint(pubkey, DB):
    address = tools.make_address([pubkey], 1)
    return {'type': 'mint',
            'pubkeys': [pubkey],
            'signatures': ['first_sig'],
            'count': tools.count(address, DB)}
def genesis(pubkey, DB):
    target_ = target.target()
    out = {'version': custom.version,
           'length': 0,
           'time': time.time(),
           'target': target_,
           'diffLength': blockchain.hexInvert(target_),
           'txs': [make_mint(pubkey, DB)]}
    out = tools.unpackage(tools.package(out))
    return out
def make_block(prev_block, txs, pubkey, DB):
    leng = int(prev_block['length']) + 1
    target_ = target.target(leng)
    diffLength = blockchain.hexSum(prev_block['diffLength'],
                                   blockchain.hexInvert(target_))
    out = {'version': custom.version,
           'txs': txs + [make_mint(pubkey, DB)],
           'length': leng,
           'time': time.time(),
           'diffLength': diffLength,
           'target': target_,
           'prevHash': tools.det_hash(prev_block)}
    out = tools.unpackage(tools.package(out))
    return out

    
def POW(block, restart_signal):
    halfHash = tools.det_hash(block)
    block[u'nonce'] = random.randint(0, 10000000000000000000000000000000000000000)
    count = 0
    while tools.det_hash({u'nonce': block['nonce'],
                          u'halfHash': halfHash}) > block['target']:
        count += 1
        block[u'nonce'] += 1
        if restart_signal.is_set():
            restart_signal.clear()
            return {'solution_found': True}
    return block