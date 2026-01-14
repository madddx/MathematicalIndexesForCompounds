import parser
import topology
from chemspipy import ChemSpider

cs = ChemSpider('k66XWXT4eY8blIm8nZprn1G7HBCqHvD4Cd0Oe0Y1')

std_in_chl_string = cs.search('tacrine')[0].inchi
print(std_in_chl_string)
print()

ids_and_elements = parser.parse_std_in_chl_string(std_in_chl_string)
print()

print(topology.find_basic_topology(ids_and_elements=ids_and_elements))
topology.compute_topological_indices_2(ids_and_elements=ids_and_elements)