from __future__ import print_function
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import pandas as pd

def RangRas(o):
    index=["color","color_name","hex","R","G","B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)

    NUM_CLUSTERS = 5

    #print('reading image')
    im = Image.open(o)
    #im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
    e = list()

    #print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    #print('Colors:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    for i in range(NUM_CLUSTERS):               # find most frequent
        peak = codes[i]
        colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')

        R=int(peak[0])
        G=int(peak[1])
        B=int(peak[2])
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                cname = csv.loc[i,"color_name"]
                e.append(csv.loc[i,"color_name"])
        #print(cname)
    index_max = np.argmax(counts)
    #print('Dominant: %s (#%s)' % (peak, colour))
    return(codes)