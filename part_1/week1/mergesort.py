# max number of inversions 
# x = n(n-1) / 2

import numpy as np
#int_list = [1,0]
#int_list = [1, 0, 3, 2]
#int_list = [2, 1, 0, 5, 4, 3, 7, 6]
#int_list = [2, 1, 5, 6, 6, 9, 8, 4]
#int_list = [1, 5, 6, 6, 9, 8, 4]
#int_list = [1,3,5,2,4,6]
#int_list = [2,1,3]
#int_list = [3,4,1,2,5,6]
#int_list = [2,1,4,3,6,5,8,7]
#int_list = [2,1,2,3]
#print int_list
txt_list = []
int_list = []
with open('./data/IntegerArray.txt', 'r') as f:
    txt_list = f.readlines()


for item in txt_list:
    int_list.append( int(item) )

array_size = len(int_list)
print 'done reading %i lines.' % (array_size)

max_num_inversions = (array_size * (array_size - 1)) / 2
print 'max_num_inversions : ', max_num_inversions

#v = 0
def merge3(array, start, split, end):
#    global v
    #print 'merging indices...', start, split, end
    
    n1 = split - start + 1
    #print 'n1 ', n1

    n2 = end - split
    #print 'n2 ', n2

    L = []
    R = []
    
    for i in xrange(n1):
        #print 'i ', i
        arr_val = array[start + i]
        #print 'L arr_val ', arr_val
        L.append(arr_val)

    for j in xrange(n2):
        #print 'j ', j
        arr_val = array[split + j + 1]
        #print 'R arr_val ', arr_val
        R.append(arr_val)

    #print 'L ', L
    #print 'R ', R

    i = 0
    j = 0
    v = 0

    for k in xrange(start, end+1):

        if i < len(L) and j < len(R):
            if L[i] <= R[j]:
                array[k] = L[i]
                i+=1
            else:
                array[k] = R[j]
                j+=1
                v += len(L) - i

        elif i >= len(L) and j < len(R):
            array[k] = R[j]
            j+=1
            v += len(L) - i

        elif i < len(L) and j >= len(R):
            array[k] = L[i]
            i+=1

    #print array
    #print v

    return v



def merge_sort3(array, start, end):
#    global v
    x = 0
    y = 0 
    z = 0
    if start < end:
        #print '~~~'
        #print 'start - end : ', start, end
        #print 'recurse.'

        a1 = (start + end) / 2
        a2 = a1 + 1
        #print 'ms[a] ', start, a1
        #print 'ms[b] ', a2, end 
        
        x = merge_sort3(array, start, a1)
        y = merge_sort3(array, a2, end)

        z = merge3(array, start, a1, end)
    
    return x + y + z

num_inv = merge_sort3(int_list, 0, array_size-1)

print 'num inv ', num_inv


    
def count_inv(array, n):
    n1 = n / 2

    b = array[:n1]
    c = array[n1:]
    d = np.zeros(n)

    i = 0
    j = 0

    for k in xrange(n):
        if b[i] < c[j]:
            d[k] = b[i]
            i+=1
        elif c[j] < b[i]:
            d[k] = c[j]
            j+=1

    return 0


def count(array, n):
    if n == 1: 
        return 0
    else:
        n1 = n / 2
        
        a1 = array[:n1]
        a2 = array[n1:]

        x = count(a1, a1.size)
        y = count(a2, a2.size)

        z = count_inv(array, n)

    return x + y + z



#a = np.array(int_list)
#count(a, a.size)

#merge_sort3(int_list, 0, array_size-1)

#print 'total inversions : ', v
