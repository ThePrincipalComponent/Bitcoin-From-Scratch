# pseudocode taken from wikipedia: Extended Euclidean Algorithm
def inv(a, p):
    old_r, r = a, p
    old_s, s = 1, 0
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
    
    return old_s % p