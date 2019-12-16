import numpy as np
from utils import diadic_expand, package, generate, merge, maximize_dict
from collections import defaultdict

# Maximum 'L' constraint
# freq_list : frequency of each character

freq_list = [7,1,4,2,5,6]
L = 3
freq_list = sorted(freq_list)
n = len(freq_list)

print("n : {}, L : {}".format(n, L))

print("Frequency list : {}".format(freq_list))
X = n-1

diadic = diadic_expand(X)
print("Diadic expansion of X(=n-1)\n{}={}".format(X, '+'.join(["2^{}".format(num) for num in diadic])))

curl = -L

coin_list_packed = list()
# All of coin is sorted in coin_list_packed
coin_ans = list()

while len(diadic)>0:
    print("===========================================================1/{}======================================================================".format(np.power(2,-curl)) if curl<0 else "==========================================================={}======================================================================".format(np.power(2,curl)))
    #  iteration 
    # curl from -L to log_2(2n) 
    # 2^L > n
    # L > log_2(n)
    # curl increase by one
    # Maximum 'O(L)' iteration
    if curl==diadic[0]:
        # If there is an element for diadic expansion
        coin = coin_list_packed.pop(0)
        print("Select {}".format(str(coin)))
        coin_ans.append(coin)
        diadic.pop(0)
        # O(1)

    if curl<0:
        coin_list_cur = generate(freq_list, curl)
        # generate 'n' elements : O(n) 
        coin_list_packed = merge(coin_list_packed, coin_list_cur)
        # len(coin_list_packed) < 2n 
        # len(coin_list_cur) = n
        # Time complexity of merge operation : O(n)
        coin_list_packed = package(coin_list_packed)
        # packing
        # pack => O(1)
        # maximum len(coin_list_packed)/2 < n => O(n)
    else:
        coin_list_packed = package(coin_list_packed)
        # packing
        # pack => O(1)
        # maximum len(coin_list_packed)/2 < n => O(n)
    curl+=1
print("====================================================================================================================================")
print("Selected coins")
print(', '.join([str(coin) for coin in coin_ans]))

freq2l = defaultdict(int) 
# Number of unpacked coins < nL = > O(nL)
for coin in coin_ans:
    print("====================================================================================================================================")
    print("For the coin {}".format(coin))
    coins_unpacked = coin.unpack_coins()
    print("Unpackaged results\n"+', '.join([str(coin) for coin in  coins_unpacked]))
    for leafcoin in coins_unpacked:
        if -leafcoin.fv > freq2l[leafcoin.rv]:
            freq2l[leafcoin.rv] = -leafcoin.fv
    #freq2l = maximize_dict(freq2l, coin.unpack(freq_list), freq_list)
print("====================================================================================================================================")
print('\n'.join(["{} has length {} code".format(freq, freq2l[freq]) for freq in freq_list]))
print("====================================================================================================================================")
