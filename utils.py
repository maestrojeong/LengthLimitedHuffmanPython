import numpy as np
from collections import defaultdict

class Coin:
    def __init__(self, rv, fv):
        self.rv = rv
        self.fv = fv
        self.subcoin = list()

    def add_sub(self, coin1, coin2):
        self.subcoin.append(coin1)
        self.subcoin.append(coin2)

    def unpack(self, keys):
        if len(self.subcoin)==0:
            freq2l = defaultdict(int)
            freq2l[self.rv] = -self.fv
            return freq2l
        else:
            freq2l = maximize_dict(self.subcoin[0].unpack(keys), self.subcoin[1].unpack(keys), keys)
            return freq2l

    def unpack_coins(self):
        # Depth x => 2^x operations 
        # Depth x < 2L => O(n)

        if len(self.subcoin)==0:
            return [self]
        else:
            return self.subcoin[0].unpack_coins() + self.subcoin[1].unpack_coins()

    def __str__(self):
        return '({}, 1/{})'.format(self.rv, np.power(2, -self.fv)) if self.fv<0 else '({}, {})'.format(self.rv, np.power(2, self.fv))

def maximize_dict(dict1, dict2, keys):
    for key in keys:
        dict1[key] = max(dict1[key], dict2[key])
    return dict1

def pack_coin(coin1, coin2):
    pcoin = Coin(coin1.rv+coin2.rv, coin1.fv+1)
    pcoin.add_sub(coin1, coin2)
    return pcoin

def diadic_expand(num):
    '''
    Args : 
        num - integer
    '''
    diadic = list()

    tmp = num 

    idx = 0

    while tmp>0:
        if tmp%2==1:
            diadic.append(idx)
        tmp = tmp//2
        idx+=1
    return diadic

def generate(freq_list, fv):
    coin_list = list()
    for freq in freq_list:
        coin_list.append(Coin(freq, fv))
    print("Generate {}".format([str(coin) for coin in coin_list]))
    return coin_list

def package(slist):
    idx = 0 
    pack = list()
    while idx+1<len(slist):
        #print("Package {}, {}".format(slist[idx], slist[idx+1]))
        pack.append(pack_coin(slist[idx], slist[idx+1]))
        idx+=2
    if idx==len(slist)-1:
        discard =  slist[idx]
        print("Discard : {}".format(discard))
    print("Packaged result : {}".format([str(coin) for coin in pack]))
    return pack

def merge(slist1, slist2):
    """
    Merge two sorted lists
    """
    if len(slist1) == 0:
        return slist2
    elif len(slist2) == 0:
        return slist1
    idx1, idx2 = 0, 0
    mlist = [] 
    total_length = len(slist1) + len(slist2)
    while len(mlist) < total_length:
        if slist1[idx1].rv <= slist2[idx2].rv:
            mlist.append(slist1[idx1])
            idx1 += 1
        else:
            mlist.append(slist2[idx2])
            idx2 += 1
        if idx2 == len(slist2):
            mlist += slist1[idx1:]
            break
        elif idx1 == len(slist1):
            mlist += slist2[idx2:]
            break
    print("Merged result : {} ".format([str(coin) for coin in mlist]))
    return mlist
