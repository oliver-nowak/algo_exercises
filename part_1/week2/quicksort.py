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
#int_list = [2,3,6,7,5,4,1]
#int_list = [1,2,3,4,5,6,7,8,9,10] #19
#int_list = [1,2,3,4,5,6,7,8] # 13
#int_list = [3,2,1,5,4,8,7,6,9,10] #19 or 21
txt_list = []
int_list = []
with open('./data/QuickSort.txt', 'r') as f:
    txt_list = f.readlines()


for item in txt_list:
    int_list.append( int(item) )

array_size = len(int_list)
print 'done reading %i lines.' % (array_size)

def get_median(a, b, c):
    if ((a >= b and a <= c) or (a >= c and a <= b)):
        return 0
    elif ((b >= a and b <= c) or (b >= c and b <= a)):
        return 1
    else:
        return 2

def partition_median(A, l, r):
    # find the median in the array between l and r
    median = 0
    distance = r - l
    
    # check if even or odd
    oo = distance % 2
    
    if oo == 1:
        #odd 
        median = (distance / 2)
    else:
        #even
        median = (distance / 2) - 1
    
    median = median + l 
    
    # set up the 'median of 3' list, containing first, middle, and last element
    p0 = A[l]
    p1 = A[median]
    p2 = A[r-1]

    # find the index of the median of the first, middle, and last element (unsorted)
    pp = get_median(p0,p1,p2)

    # swap the median element with the first element
    if pp == 0:
        tmp = A[l]
        A[l] = A[l]
    
    elif pp == 1:
        tmp = A[l]
        A[l] = A[median]
        A[median] = tmp

    elif pp == 2:
        tmp = A[l]
        A[l] = A[r-1]
        A[r-1] = tmp
    
    #set the first element as the pivot
    p = A[l]
    i = l + 1
    
    # calculate the number of elements to compare
    v = (r - l) - 1

    # iterate through the array comparing elements against the pivot, swapping
    # as needed
    for j in xrange(l+1, r):
        if A[j] <= p:
            tmp = A[j]
            A[j] = A[i]
            A[i] = tmp
            i += 1

    #swap the pivot element with the last element < pivot
    tmp = A[l]
    A[l] = A[i-1]
    A[i-1] = tmp
    
    return i, v

def partition_last_element(A, l, r):
    # swap 1st and last element, since we are using last element as pivot
    tmp = A[l]
    A[l] = A[r-1]
    A[r-1] = tmp

    #set the first element as the pivot
    p = A[l]
    i = l + 1
    
    # calculate the number of elements to compare (part of homework)
    v = (r - l) - 1

    #iterate through the array comparing elements against the pivot, swapping
    # as needed
    for j in xrange(l+1, r):
        if A[j] <= p:
            tmp = A[j]
            A[j] = A[i]
            A[i] = tmp
            i += 1
    # swap the pivot element with the last element < pivot
    tmp = A[l]
    A[l] = A[i-1]
    A[i-1] = tmp

    return i, v

def partition(A, l, r):
    # set the pivot to the first element
    p = A[l]
    i = l + 1
    
    # calculate the number of elements to compare (part of homework)
    v = (r - l) - 1
    
    # iterate through the array comparing elements against the pivot, swapping
    # as needed
    for j in xrange(l+1, r):
        if A[j] <= p:
            tmp = A[j]
            A[j] = A[i]
            A[i] = tmp
            i += 1

    #swap the pivot element with the last element < pivot
    tmp = A[l]
    A[l] = A[i-1]
    A[i-1] = tmp

    return i, v

def quicksort(A, p, r):
    # num of comparisons counter (not part of the algo; part of the homework)
    x = 0
    y = 0
    z = 0
    # check if you are trying to sort a 1 element array (which by definition
    # is already sorted) - this is the base-case, and represents the 'bottom'
    # of the recursion tree.
    if p < r:
        # partition the array: 3 different ways to find pivot:
        # 1 - via first element
        # 2 - via last element
        # 3 - via a median of 3 (first, middle, last)
        q, x = partition(A, p, r) #162085
        #q , x = partition_last_element(A, p, r) #164123
        #q , x = partition_median(A, p, r) #!150657 !153978 !135125
        
        # recurse, according to the partitions
        y = quicksort(A, p, q - 1)
        z = quicksort(A, q, r) 
    
    # add up the num of comparisions (part of the homework)
    return x + y + z


list_size = len(int_list)
print 'list size : ', list_size

num_comparisons = quicksort(int_list, 0, list_size)

#print 'sorted : ', int_list
print 'num_comparisons : ', num_comparisons

