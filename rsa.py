#!/usr/bin/env python

from random import getrandbits, randrange
import logging


def is_prime(n,k=32):
    logging.debug(f"n={n},k={k}")
    if n <=3:
        if n>=2:
            logging.debug("2 or 3")
            return True
        else:
            logging.debug("< 2")
            return False
    
    if n % 2 == 0:
        logging.debug("n is even")
        return False

    # Find d and r
    d = n - 1
    r = 0

    ## Begin loop
    
    d = int(d/2)
    r = r + 1
    logging.debug(f"1. n-1 loop => d={d},r={r}")
    while d % 2 == 0 and d!= 0:        
        d = int(d/2)
        r = r + 1
        logging.debug(f"1. n-1 loop => d={d},r={r}")
    
    for _ in range(k):
        a = randrange(2,n-2)
        x = pow(a,d,n)
        logging.debug(f"a={a},x={x}")
        if x == 1 or x == n - 1:
            logging.debug("x == 1 or x == n - 1")
            continue
        broke = False
        for _ in range(r-1):
            x = pow(x,2,n)
            logging.debug(f"x={x}")
            if x == 1:
                logging.debug("x == 1")
                return False
            if x == n-1:
                logging.debug("x == n - 1")
                broke = True
                break
        if not broke:
            return False # if we finish the inner loop, number is composite

    return True

def genprime(l):
    n=getrandbits(l) | (1 + 2**(l - 1))
    while not is_prime(n):
        n += 2
    return n

def egcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def genmod(p, q):
    phi = (p - 1) * (q - 1)

    e = randrange(2, phi - 1)
    r,u,v = egcd(e, phi)
    while r != 1:
        e = randrange(2, phi - 1)
        r,u,v = egcd(e, phi)

    if u < 0:
        k = 0
        while u + k * phi < 2 and u + k * phi > phi:
            k += 1
        
        u = u + k * phi

    M = p * q

    return (M,e), u 

def enc(m,pkey):
    M,e = pkey
    return pow(m,e,M)

def dec(c,pkey,skey):
    M,_ = pkey
    return pow(c,skey,M)

def encmsg(s,pkey):
    res = []
    for c in s:
        res.append(enc(ord(c),pkey))
    return res

def decmsg(s,pkey,skey):
    res = []
    for i in s:
        res.append(dec(i,pkey,skey))
    res = list(map(chr,res))
    return res

def keygen(l):
    p = genprime(l)
    q = genprime(l)
    return genmod(p,q)

if __name__ == "__main__":
    import sys
    import getopt

    logging.basicConfig(format='%(levelname)-5s : %(message)s',level=logging.INFO)

    def usage():
        print(f"Usage : {sys.argv[0]} --prime ") 

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:g:m:k:hd', ['prime=','genprime=','genmod=','genkey=','enc=','pkey=','skey=',"dec=", 'help','debug'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    prime = None
    genp = None
    genm = None
    pkey = None
    skey = None
    encMsg = None
    decMsg = None


    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-p', '--params'):
            prime = int(arg)
        elif opt in ('-g', '--genprime'):
            genp = int(arg)
        elif opt in ('-m', '--genmod'):
            genm = tuple(map((lambda x: int(x)),arg.split(",")))
        elif opt in ('-k', '--genkey'):
            genp = int(arg)
        elif opt in ('--enc'):
            encMsg = arg
        elif opt in ('--dec'):
            decMsg = arg
        elif opt in ('--pkey'):
            pkey = tuple(map((lambda x: int(x)),arg.split(",")))
        elif opt in ('--skey'):
            skey = int(arg)
        elif opt in ('-d','--debug'):
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            usage()
            sys.exit(2)

    if prime != None:
        logging.info(is_prime(prime))

    if genp != None:
        logging.info(genprime(genp))

    if genm != None:
        logging.info(genmod(*genm))

    if encMsg != None:
        if pkey == None:
            (M,e),u = keygen(32)
            s = encmsg(encMsg,(M,e))
            logging.info(s)
            s = decmsg(s,(M,e),u)
            logging.info(s)
