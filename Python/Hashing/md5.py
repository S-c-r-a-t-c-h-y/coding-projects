
from math import floor, sin


k = [floor(abs(2**32 * sin(i + 1))) for i in range(64)]

def md5(message: bytes):
    n = len(message)
    message += b"1"
    
    while len(message) % 512 != 448:
        message += b"0"
        
    message += n.to_bytes(length=64, byteorder='little')

    
md5(b"12345678")