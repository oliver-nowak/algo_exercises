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

def merge(array, start, split, end):
    n1 = split - start + 1
    n2 = end - split

    L = []
    R = []
    
    for i in xrange(n1):
        arr_val = array[start + i]
        L.append(arr_val)

    for j in xrange(n2):
        arr_val = array[split + j + 1]
        R.append(arr_val)

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

    return v



def merge_sort(array, start, end):
    x = 0
    y = 0 
    z = 0
    if start < end:
        a1 = (start + end) / 2
        a2 = a1 + 1
        
        x = merge_sort(array, start, a1)
        y = merge_sort(array, a2, end)

        z = merge(array, start, a1, end)
    
    return x + y + z

num_inv = merge_sort(int_list, 0, array_size-1)


print 'number of inversions : ', num_inv
