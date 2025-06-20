from typing import Tuple, DefaultDict
from element import Element
from collections import defaultdict, deque
import math

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


def compute_topological_indices(ids_and_elements: dict[int, Element], rr_alpha: float = 1.0) -> None: 
    # rr_alpha is a parameter used in calculating the Reciprocal Randić Index.
    # It defaults to 1.0 if not provided
    # None. This function only prints the calculated indices; it does not return them.


    visited_edges = set() # a set to keep track of visited edges to avoid double counting 
    M1 = M2 = HM = H = mm2 = ReZG3 = F = 0.0 # this will set the initial values to 0
    IS = A = R = RR = ABC = SC = 0.0

    
    for u in ids_and_elements.values(): # Iterate through all elements in the graph
        for v in u.connections: # For each connection of the current element
            if (u.id, v.id) in visited_edges or (v.id, u.id) in visited_edges: # Skip if this edge has already been processed
                continue

            du = len(u.connections) # number of connections of node u
            dv = len(v.connections) # number of connections of node v

            M1 += (du + dv) # First Zagreb Index: M1 = Σ (du + dv)
            M2 += (du * dv) # Second Zagreb Index: M2 = Σ (du * dv)
            HM += (du + dv) ** 2 # Hyper Zagreb Index: HM = Σ (du + dv)²
            H += 2 / (du + dv) # Harmonic Index: H = Σ 2 / (du + dv)
            mm2 += 1 / (du * dv) # Second Modified Zagreb Index: mm2 = Σ 1 / (du * dv)
            ReZG3 += (du * dv) * (du + dv) # Redefined Third Zagreb Index: ReZG3 = Σ (du * dv) * (du + dv)
            F += du ** 2 + dv ** 2 # Forgotten Index: F = Σ (du² + dv²)
            IS += (du * dv) / (du + dv) # Inverse Sum Indegree Index: IS = Σ (du * dv) / (du + dv)
            
            if du + dv - 2 != 0: #to avoid denominator being zero
                A += ((du * dv) / (du + dv - 2)) ** 3 # Augmented Zagreb Index: A = Σ ((du * dv) / (du + dv - 2))³
            
            R += 1 / math.sqrt(du * dv) # Randić Index: R = Σ 1 / √(du * dv)
            RR += 1 / ((du * dv) ** rr_alpha) # Reciprocal Randić Index: RR = Σ 1 / (du * dv) ^ α

            if du * dv != 0: #to avoid denominator being zero
                ABC += math.sqrt((du + dv - 2) / (du * dv)) # Atomic Bond Connectivity Index: ABC = Σ √((du + dv - 2) / (du * dv))
 
            SC += 1 / math.sqrt(du + dv) # Sum-connectivity Index: SC = Σ 1 / √(du + dv)

            visited_edges.add((u.id, v.id)) # Mark this edge as visited to avoid double counting

    print("\nTopological Indices:")
    print(f"First Zagreb Index (M1): {M1}") # First Zagreb Index
    print(f"Second Zagreb Index (M2): {M2}") # Second Zagreb Index
    print(f"Hyper Zagreb Index (HM): {HM}") # Hyper Zagreb Index
    print(f"Harmonic Index (H): {H:.4f}") # Harmonic Index
    print(f"Second Modified Zagreb Index (mm2): {mm2:.4f}") # Second Modified Zagreb Index
    print(f"Redefined Third Zagreb Index (ReZG3): {ReZG3}") # Redefined Third Zagreb Index
    print(f"Forgotten Index (F): {F}") # Forgotten Index
    print(f"Inverse Sum Indegree Index (IS): {IS:.4f}") # Inverse Sum Indegree Index
    print(f"Augmented Zagreb Index (A): {A:.4f}") # Augmented Zagreb Index
    print(f"Randic Index (R): {R:.4f}") # Randic Index
    print(f"Reciprocal Randic Index (RRalpha, alpha={rr_alpha}): {RR:.4f}") # Reciprocal Randic Index
    print(f"Atomic Bond Connectivity Index (ABC): {ABC:.4f}") # Atomic Bond Connectivity Index
    print(f"Sum-connectivity Index (SC): {SC:.4f}") # Sum-connectivity Index
