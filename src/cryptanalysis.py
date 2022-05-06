#!/usr/bin/env python

import logging
from src.freq import monograms,bigrams,quadgrams,words
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def cryptanalysis(msg):
    freq = {k:0 for k in letters}

    for c in msg:
        freq[c]+=1

    freq = {k: v/len(msg) for k, v in freq.items()}
    freq = reversed(sorted(freq.items(), key=lambda x:x[1]))
    freq = dict(freq)
    logging.debug(freq)
    logging.debug(monograms.freqs)
    print(len(freq.keys()),len(monograms.freqs.keys())) 

    mapping = {k[0]:k[1] for k in zip(freq.keys(),monograms.freqs.keys())}

    logging.debug(mapping)

    msg = "".join(str(x) for x in [mapping[x] for x in msg])


    
    return msg

if __name__ == "__main__":
    import sys, getopt
    logging.basicConfig(format='%(levelname)-5s : %(message)s',level=logging.INFO)

    def usage():
        print(f"Usage : {sys.argv[0]} [--help] [--debug]") 

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dh', ['debug','help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-d','--debug'):
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            usage()
            sys.exit(2)

    msg = "LIVITCSWPIYVEWHEVSRIQMXLEYVEOIEWHRXEXIPFEMVEWHKVSTYLXZIXLIKIIXPIJVSZEYPERRGERIMWQLMGLMXQERIWGPSRIHMXQEREKIETXMJTPRGEVEKEITREWHEXXLEXXMZITWAWSQWXSWEXTVEPMRXRSJGSTVRIEYVIEXCVMUIMWERGMIWXMJMGCSMWXSJOMIQXLIVIQIVIXQSVSTWHKPEGARCSXRWIEVSWIIBXVIZMXFSJXLIKEGAEWHEPSWYSWIWIEVXLISXLIVXLIRGEPIRQIVIIBGIIHMWYPFLEVHEWHYPSRRFQMXLEPPXLIECCIEVEWGISJKTVWMRLIHYSPHXLIQIMYLXSJXLIMWRIGXQEROIVFVIZEVAEKPIEWHXEAMWYEPPXLMWYRMWXSGSWRMHIVEXMSWMGSTPHLEVHPFKPEZINTCMXIVJSVLMRSCMWMSWVIRCIGXMWYMX"

    logging.info(cryptanalysis(msg))