"""Kosaraju's algorithm for computing strongly connected components in a 
directed acyclic graph"""

import copy
import operator
import sys 

# sets the recursion limit to a large amount
# this is needed for files larger than 1MB
sys.setrecursionlimit(1000000)

raw_list = []

rev_raw_list = []

# adjacency list for the graph
adj_list = []

# reversed adjacency list 
rev_adj_list = []

# finishing times list
finish_dict = {}

# leader list
leader_dict = {}

# number of nodes processed so far
t = 0

# current source vertex
s = None

sorted_finish_dict = {}

FILE_URL = './data/test_case_06.txt'

def init_finish_dict(graph):
    """This method initializes the finishing time data structure."""

    finish_dict = {}
    leader_dict = {}
    for node in graph:
        node_label = node[0]
        finish_dict[node_label] = 0
        leader_dict[node_label] = 0

    return finish_dict, leader_dict

def consolidate_nodes(node_list):
    """This function consolidates a list of nodes and their destination arcs, 
    already in sorted order, into a new list which describes one list item as
    one node. each node will contain a node label, a list of arcs, and a flag
    denoting explored status.

    Data Structure:
        [label, [list of arcs], explored?]

    Data Type:
        [int, list, bool]
    
    Input:
        [1, 2]
        [1, 3]
        [2, 3]

    Output:
        [1, [2, 3],False]
        [2, [3], False]
    """
    consolidated_node_list = []
    node_index = 0
    node = []
    arcs = []

    for item in node_list:
        # check if we are iterating over a new node and add to the list or reset
        if item[0] != node_index:
            
            # check if the arc list contains any arcs before we reset
            if (len(arcs) > 0):
                # add the list of arcs to the node
                node.append(arcs)

                # add exploration status
                node.append(False)

                # add the node to the list
                consolidated_node_list.append(node)
            
            # reset the node data structures
            node = []
            arcs = []
            node_index = item[0]
            node.append(node_index)
        
        # add the destination vertex to the node, creating an arc
        arcs.append(item[1])

    # add the last node to the list
    node.append(arcs)
    node.append(False)
    consolidated_node_list.append(node)

    return consolidated_node_list


def load_data():
    """This function loads the data into a raw list for later configuration.
    It returns both a raw adjacency list, and its reversed adjacency list."""

    raw_list = []
    rev_raw_list = []
    with open(FILE_URL, 'r') as f:
        for line in f:
            line = line.strip('\r\n')
            fields = line.split()
            row = []
            for field in fields:
                row.append(int(field))

            # copy the list 
            rev_row = copy.deepcopy(row)

            # reverse the arc
            rev_row.reverse()
    
            # append to a raw list - no assumptions are made if the inputs are
            # already sorted
            raw_list.append(row)
            rev_raw_list.append(rev_row)

        # sort the raw lists in ascending order in case elements are mixed
        raw_list.sort()
        rev_raw_list.sort()

        # reverse list to sort in descending order for DFS_Loop
        raw_list.reverse()
        rev_raw_list.reverse()

        return raw_list, rev_raw_list


def depth_first_search(graph, node):
    global t
    global finish_dict
    
    current_node = node[0]
#    print 'at node : ', current_node
    # set the node exploration status
    node[2] = True

    # get the arc list from the node
    arc_list = node[1]
    arc_list.reverse()
#    print 'arc list ', arc_list
    
    # iterate over the list of arcs
    for arc in arc_list:
#        print 'looking at ', arc

        for dest_node in graph:
            if dest_node[0] == arc:
#                print 'found dest at ', dest_node[0]
                if dest_node[2] == False:
#                    print 'not explored !'
                    depth_first_search(graph, dest_node)
#                else:
#                    print 'EXPLORED LEAVING'
                #    break
        


    t += 1
#    print 'node ', current_node
#    print 't ', t
    finish_dict[current_node] = t
#    print finish_dict
    
    

def depth_first_search_loop(graph):
    global t

    t = 0

    for node in graph:
#       print 'label ', node[0]
       
       if node[2] is False:
#            print 'exploring ...'
            depth_first_search(graph, node)
  

def dfs(graph, node):
    global s
    global leader_list

    node[2] = True
    leader_dict[s] += 1

    arc_list = node[1]

    for arc in arc_list:
        for dest_node in graph:
            if dest_node[0] == arc and dest_node[2] == False:
#                if dest_node[2] == False:
                    dfs(graph, dest_node)


  

def dfs_loop(graph):
    global s
    global finish_dict
    global sorted_finish_dict
    
    s = None
    
    for i in sorted_finish_dict:
        label = i
#        print '---'
#        print 'getting label ', label
#        print 'node ', label[0]
#        print 'f_time ', label[1]

        for node in graph:
            if node[0] == label[0] and node[2] == False:
#                print 'found node...', node[0]
                s = node[0]

                dfs(graph, node)


print '>>> loading data...'
raw_list, rev_raw_list = load_data()

print '>>> consolidating raw list...'
adj_list     = consolidate_nodes(raw_list)

print '>>> consolidating reversed raw list...'
rev_adj_list = consolidate_nodes(rev_raw_list)

print '>>> initializing the dfs dicts...'
finish_dict, leader_dict  = init_finish_dict(adj_list)

#for node in rev_adj_list:
#    print node

print '>>> starting first pass of dfs...'
depth_first_search_loop(rev_adj_list)

#print 'finish_dict : ', finish_dict

# returns tuples in (node_label, finish_time) in descending order
sorted_finish_dict = sorted(finish_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

#print 'sorted finish dict :', sorted_finish_dict
print '>>> starting second pass of dfs...'
dfs_loop(adj_list)

#print 'leader_list : ', leader_dict
sorted_leaders = sorted(leader_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
#print 'sorted_leaders : ', sorted_leaders
#print 'finish_dict : ', finish_dict


print '--> top 5 SCC Leaders '
for i in xrange(5):
    print '> ', sorted_leaders[i][1]



    
