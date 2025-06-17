from typing import Tuple, DefaultDict
from element import Element
from collections import defaultdict, deque

def find_basic_topology(ids_and_elements: DefaultDict[int, Element]) -> DefaultDict[Tuple[int, int], int]:

    # a set that we will use to not find basic topology for an element more than once
    visited = set()

    # a hashmap that says which valency pairs occured how many times
    basic_topology = defaultdict(int)
    
    starting_element = ids_and_elements[1] # start from the first element
    visited.add(starting_element) # add this element as visited first

    bfs_queue = deque() # bfs_queue, basically a queue to say which elements we should visit next
    bfs_queue.append(starting_element) # append the starting element to the queue

    while bfs_queue: # while there are elements in the queue
        ith_element = bfs_queue.popleft() # pop out an element

        for connection in ith_element.connections: # go through all connections
            if connection not in visited: # if connection has not already been seen before
                '''
                 * NOTE
                 * valency pairs go both way, for example let us consider a bond C-H
                 * valency of carbon is 4 and valency of hydrogen is 1
                 * so two pairs can be produced from this bond alone which are as follows:
                 * pair1 = (4, 1) [valency of carbon, valency of hydrogen]
                 * pair2 = (1, 4) [valency of hydrogen, valency of carbon]
                 * thus, order of the valency matters
                 * however a pair of (1, 4) made from connection between chlorine and carbon and
                 * a pair of (1, 4) made from connection between hydrogen and carbon are equivalent
                 *
                 * the above stated rules apply for all bonds
                '''

                element_valencies = [] # declare a list that will hold two numbers (valency pair)
                element_valencies.append(ith_element.valency) # append the valenciess
                element_valencies.append(connection.valency)

                basic_topology[tuple(element_valencies)] += 1 # increment frequency of that valency pair in the hash map

                element_valencies = element_valencies[::-1] # reverse the list
                basic_topology[tuple(element_valencies)] += 1 # increment frequency of the reversed valency pair in the hash map

                bfs_queue.append(connection) # append this connection to visit next
                visited.add(connection) # since we know we will visit this next, we can just add this to the visited set prematurely

    return dict(basic_topology) # return the basic topology hashmap