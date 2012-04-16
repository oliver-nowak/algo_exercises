"""Kosaraju's algorithm for computing strongly connected components in a 
directed acyclic graph"""

import copy
import operator
import sys
import thread
import threading
import time

# raw list from the file
raw_list = []

# reversed raw list from the file
rev_raw_list = []

# adjacency list for the graph
adj_list = []

# reversed adjacency list 
rev_adj_list = []

# adjacency list as dict
adj_dict = {}

# reversed adjacency list as dict
rev_adj_list = {}

# finishing times list
finish_dict = {}

# leader list
leader_dict = {}

# number of nodes processed so far
t = 0

# current source vertex
s = None

# sorted keys for the finishing time dict
sorted_finish_dict = {}

FILE_URL = './data/test_case_04.txt'

def init_dfs_dicts(graph):
    """This method initializes the finishing time data structure."""
    
    finish_dict = {}
    leader_dict = {}
    for node in graph:
        finish_dict[node] = 0
        leader_dict[node] = 0

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
    node_index = 0
    node = []
    arcs = []
    con_dict = {}

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
                con_dict[node_index] = node
            
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
    con_dict[node_index] = node
    
    return con_dict


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
    
    # set the node exploration status
    node[2] = True

    # get the arc list from the node
    arc_list = node[1]
    arc_list.reverse()
    
    # iterate over the list of arcs
    for arc in arc_list:
        try:
            dest_node = graph[arc]

            if dest_node[2] == False:
                depth_first_search(graph, dest_node)
        except KeyError:
            continue


    t += 1
    finish_dict[current_node] = t
    
    

def depth_first_search_first_pass(keys, graph):
    global t

    t = 0
    
    # iterate through a reversed adjacency list 
    for node in keys:
       vert = graph[node]

       if vert[2] is False:
            depth_first_search(graph, vert)  

def dfs(graph, node):
    global s
    global leader_dict

    node[2] = True
    leader_dict[s] += 1

    arc_list = node[1]

    # iterate through the arcs that the node contains
    for arc in arc_list:
        if arc in graph:
            dest_node = graph[arc]

            if dest_node[2] == False:
                dfs(graph, dest_node)  

def depth_first_search_second_pass(sorted_keys, graph):
    global s

    s = None
    
    # iterate through finishing time list, in descending order
    for i in sorted_keys:
        vert = i[0]
        if vert in graph:

            node = graph[vert]

            if node[2] is False:
                s = i[0]
                dfs(graph, node)



def start():
    # init the globals 
    global raw_list, rev_raw_list, adj_dict, rev_adj_dict, rev_sort_dict_keys, finish_dict, leader_dict, sorted_finish_dict, sorted_leaders
    print '>>> loading data...'
    raw_list, rev_raw_list = load_data()

    print '>>> consolidating raw list...'
    adj_dict     = consolidate_nodes(raw_list)

    print '>>> consolidating reversed raw list...'
    rev_adj_dict = consolidate_nodes(rev_raw_list)

    rev_sort_dict_keys = list(sorted(rev_adj_dict.keys(), reverse=True))

    print '>>> initializing the dfs dicts...'
    finish_dict, leader_dict  = init_dfs_dicts(adj_dict)

    print '>>> starting first pass of dfs...'
    depth_first_search_first_pass(rev_sort_dict_keys, rev_adj_dict)

    # returns list of finishing times as tuples (node_label, finish_time) in descending order
    sorted_finish_dict = sorted(finish_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    print '>>> starting second pass of dfs...'
    depth_first_search_second_pass(sorted_finish_dict, adj_dict)

    # sort the SCC's according to size, in descending order
    sorted_leaders = sorted(leader_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    print '--> top 5 SCC Leaders '
    for i in xrange(5):
        print '> ', sorted_leaders[i][1]




if __name__ == '__main__':

    # sets the recursion limit to a large amount
    # this is needed for files larger than 1MB
    sys.setrecursionlimit(1000000)

    # set the thread stack size
    # this is needed for large files, otherwise the process segfaults
    thread.stack_size(2**27)      

    # start a thread and load the algo
    t1 = threading.Thread( target = start )  

    # begin wall time 
    begin = time.clock()
    t1.start()      
    t1.join()       
    print "wall-time to process top 5 SCC's (in seconds): ", time.clock() - begin    
