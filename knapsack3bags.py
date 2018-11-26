"""
Created on Mon Nov 26 16:36:53 2018

@author: johannes
"""



import numpy as np
items = np.array(['cake', 'plant', 'TV', 'pepernoten'])



# Our Method for 2 bags
def weirdPowerSet(items):
    """ try to stick to the binary solution, but instead
        1. draw more numbers/binary combinations   2**(N*2) instead of 2**N
            the assumption is that 2**(N*2) - x == 3**N
            where x is the number of skipped numbers (see 3.)
        2. map them into onto two different bags
            e.g. number is i = 16   so,   np.binary_repr(16) = '10000'
            this number has to provide information about "taking the item" for two bags
            so, with 4 items we need 2*4=8 bits of information
            so, we use   np.binary_repr(16, 8) = '00010000'   in order to pad zeros to get 8 bits
        3. we have to avoid a situation in which we put an item into both bags at once
        4. similarly we have to avoid a situation in
        
        Caveat: building a generator would be awkward because 
            you have to yield a result every time 
        """
    N = len(items)
    combo = []
    
    # initialize counter for garbage solutions
    x = 0
    
    # get information (numbers)
    for i in range(2**(N*2)): 
        
        # map information into a binary code of sufficient length
        #   use list comprehension to cast characters as integers
        both = [int(ix) for ix in list(np.binary_repr(i, 2*N))] 
        # use the first half of the binary code as information for the first bag
        #   prepare for logical indexing by casting of integers as booleans
        index1 = np.array(both[:N], dtype=bool) 
        # use the 2nd half as info for the 2nd bag
        index2 = np.array(both[N:], dtype=bool)
        
        # discard combinations that would place an item into both bags at once
        if any(index1*index2): 
            # count those garbage solutions
            x += 1
            pass
        
        # accept all other cobinations
        #   use logical indexing to get items
        else:
            combo.append([items[index1].tolist(), items[index2].tolist()])
    
    return combo, x


pSet, x = weirdPowerSet(items)



# Their Method (gold standard) adapted for 2 bags 
def powerSet2(items):
    """returns a generator"""
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(3**N):
        combo = ([], [])
        for j in range(N):
            # test bit jth of integer i
            if (i // 3**j) % 3 == 1:
                combo[0].append(items[j])
            if (i // 3**j) % 3 == 2:
                combo[1].append(items[j])
        yield combo


def powerSet2_1(items):
    """returns a list (of list(of lists))"""
    N = len(items)
    combo = []
    # enumerate the 2**N possible combinations
    for i in range(3**N):
        combo1 = []
        combo2 = []
        for j in range(N):
            # test bit jth of integer i
            if (i // 3**j) % 3 == 1:
                combo1.append(items[j])
            if (i // 3**j) % 3 == 2:
                combo2.append(items[j])
        combo.append([combo1, combo2])
    return combo


gs_pSet = powerSet2_1(items)



# Verification 1
if ((2**(len(items)*2)) - x) == (3**len(items)):
    print("Success1: \t Both implementations resulted in the same number of combinations.")
    print(str((2**(len(items)*2)) - x) + " = 2**(N*2) = " + str(3**len(items)) + " = 3**N")
else:
    print("Fail1: \t The two implementations resulted in a different number of combinations.")
    print(str((2**(len(items)*2)) - x) + " = 2**(N*2) != " + str(3**len(items)) + " = 3**N")




# Verification 2
if sorted(pSet) == sorted(gs_pSet):
    print("Success2: \t Both implementations resulted in identical combinations.")
else:
    print("Fail2: \t The two implementations did NOT result in identical combinations.")
    
    
    
    
    
    
    
# Generator implementation using absolutely excessive list comprehension
def powerSet2_1(items):
    """returns a generator"""
    N = len(items)
    comboI =  [[c[0], c[1]] for c in [[b[:N], b[N:]] for b in [np.array(list(np.binary_repr(i, 2*N)), dtype=int).astype(bool) for i in range(2**(N*2))]] if not any(c[0]*c[1])]
    
    for i in range(len(comboI)):
        yield ([items[comboI[i][0]], items[comboI[i][1]]])
    
    
    
pGen = powerSet2_1(items)
for i in range(3**len(items)):
    print(next(pGen))
    
    
    
    
    
    
    
    
    
    
