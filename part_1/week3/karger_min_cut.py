
import math
import random
import copy


def load_data():
    """Load the data as an adjacency list. This assumes the file is delimited
    by spaces."""

    adj_list = []
    with open('./data/kargerAdj.txt', 'r') as f:
        for line in f:
            line = line.strip('\r\n')
            fields = line.split()
            row = []
            for field in fields:
                row.append(int(field))

            adj_list.append(row)

    return adj_list


def find_min_cut(adj_list):
    """Finds the minimum cut of the provided adjacency list"""

    while len(adj_list) > 2:
        # randomly choose a node from the adjacency list
        rand1 = random.randint(0, len(adj_list) - 1)
        node1 = adj_list[rand1]

        # randomly choose a node that shares an edge with the node chosen above
        rand2 = random.randint(1, len(node1) - 1 )
        chosen_node = node1[rand2]
        
        # iterate over the adjacency list to find the chosen node because the
        # list changes every iteration as a result of nodes being deleted below
        node2 = None
        for node in adj_list:
            if node[0] == chosen_node:
                node2 = node

        # now that both nodes (and therefore and edge) has been chosen, save
        # them in discrete local vars 
        vert1 = node1[0]
        vert2 = node2[0]

        vert_list = []
        
        # add all the verts in node1 into a new list, as long as its not itself
        for vert in node1[1:]:
            if vert != vert2:
                vert_list.append(vert)
        
        # add all the verts in node2 into a new list, as long as its not itself
        for vert in node2[1:]:
            if vert != vert1:
                vert_list.append(vert)
        
        # replace the verts in node1, with the new list created above
        adj_list[rand1][1:] = vert_list
   
        # go through every vert in node2, find the matching node in the 
        # adjacency list, and replace references to node2 with node1
        for node in node2[1:]:
            for i, node1 in enumerate(adj_list):
                if node1[0] == node:
                    for j, vert in enumerate(adj_list[i][1:]):
                        if vert == vert2:
                            adj_list[i][j+1] = vert1

        # iterate through the adjacency list to find node2, and delete it when
        # found. we do this instead of referencing by index, because the list
        # is _not_ invariant; rather, it changes every iteration.
        for i,node in enumerate(adj_list):
            if node[0] == vert2:
                del adj_list[i]

    #return min_cut as total of all nodes (except for label in [0])
    return len(adj_list[0][1:])


def run_min_cut(memo_adj_list, n_iterations=1):
    """Runs the min cut algorithm N iterations and returns the minimum cut"""

    # set the minimum cut to be the maximum number of cuts calculated for this
    # size of adjacency list
    memo_min_cut = 2**len(memo_adj_list)

    # iterate the min_cut algorithm
    for i in xrange(n_iterations):
        # create a new list object
        adj_list = copy.deepcopy(memo_adj_list)

        # run the algo
        min_cut = find_min_cut(adj_list)
        
        # compare the returned minimum cut, and save it if its smaller
        if min_cut < memo_min_cut:
            memo_min_cut = min_cut

    return memo_min_cut


# load data into a list
memo_adj_list = load_data()

# get size of list
n = len(memo_adj_list)

# calculate the number of iterations for a high probablity of success
# karger isnt that great unless you iterate many times in order to increase
# the chances that the minimum cut will be found
n_iterations = int(n*n*math.log(n))

# run the min_cut and return 
min_cut = run_min_cut(memo_adj_list, n_iterations)

print '>>> MIN CUT : ', min_cut
#3
