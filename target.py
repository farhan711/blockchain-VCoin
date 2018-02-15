import blockchain, custom, tools
try:
    from cdecimal import Decimal
except:
    from decimal import Decimal
    tools.log('This would run much faster if you installed cdecimal.')
memoized_weights=[custom.inflection**i for i in range(1000)]
def denominator_limited_sum(l, a=0):
    if len(l)==0: return a
    return denominator_limited_sum(l[1:], (a+l[0]).limit_denominator())
def target(length=0):
    """ Returns the target difficulty at a paticular blocklength. """
    db_length=tools.db_get('length')
    if length == 0: length = db_length
    if length < 4: return '0' * 4 + 'f' * 60  # Use same difficulty for first few blocks.
    trgs=tools.db_get('targets')
    if length <= db_length and str(length) in trgs:
        return trgs[str(length)]  
    def targetTimesFloat(target, number):
        a = int(str(target), 16)
        b = int(a * number)#this should be rational multiplication followed by integer estimation
        return tools.buffer_(str(hex(b))[2: -1], 64)
  