import parser
import topology
from chemspipy import ChemSpider

compound_names = ['tacrine', 'donepezil', 'rivastigmine', 'galantamine', 'huperzine A']
cols = ['M1', 'M2', 'HM', 'H', 'mm2', 'ReZG3', 'F', 'IS', 'A', 'R', 'RR', 'ABC', 'SC']
cs = ChemSpider('k66XWXT4eY8blIm8nZprn1G7HBCqHvD4Cd0Oe0Y1')
indices = []

for name in compound_names:
    print()
    print(f"{name}:")
    std_in_chl_string = cs.search(name)[0].inchi
    ids_and_elements = parser.parse_std_in_chl_string(std_in_chl_string)
    indices.append(topology.compute_topological_indices_2(ids_and_elements=ids_and_elements))

import pandas as pd
df = pd.DataFrame(indices, columns=cols)
df.to_csv('indices_data.csv', index=False)