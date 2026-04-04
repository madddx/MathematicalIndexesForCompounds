from collections import deque
from rdkit import Chem
import math

def dve(v: Chem.rdchem.Atom) -> int:
    neighborhood = set([v] + list(v.GetNeighbors()))

    edges = set()
    for u in neighborhood:
        for w in list(u.GetNeighbors()):
            # if w in neighborhood:
            edge = tuple(sorted((u.GetIdx(), w.GetIdx())))
            edges.add(edge)

    return len(edges)

def compute_dve_map(ids_and_elements):
    return {
        i: dve(atom)
        for i, atom in ids_and_elements.items()
    }

def compute_ve_topological_indices(ids_and_elements: dict[int, Chem.rdchem.Atom], dve_map: dict[int, int], rr_alpha: float = 1.0):
    # rr_alpha is a parameter used in calculating the Reciprocal Randić Index.
    # It defaults to 1.0 if not provided
    # None. This function only prints the calculated indices; it does not return them.

    visited_edges = set() # a set to keep track of visited edges to avoid double counting 
    M1 = M2 = HM = H = mm2 = ReZG3 = F = 0.0 # this will set the initial values to 0
    IS = A = R = RR = ABC = SC = 0.0
    
    for u in ids_and_elements.values(): # Iterate through all elements in the graph
        for v in u.GetNeighbors(): # For each connection of the current element
            edge = tuple(sorted((u.GetIdx(), v.GetIdx())))
            if edge in visited_edges:
                continue

            du = dve_map[u.GetIdx()]
            dv = dve_map[v.GetIdx()]

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

            visited_edges.add(edge) # Mark this edge as visited to avoid double counting
            
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
    
    return [M1, M2, HM, H, mm2, ReZG3, F, IS, A, R, RR, ABC, SC]

def compute_topological_indices(ids_and_elements: dict[int, Chem.rdchem.Atom]):
    dve_map = compute_dve_map(ids_and_elements)
    return compute_ve_topological_indices(ids_and_elements, dve_map)
