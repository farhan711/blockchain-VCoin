
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