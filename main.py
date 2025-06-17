import helper
import parser
import topology

file_path = r"D:\Education\Code Bases\Python\StdInChlParser\std_in_chl_string3.text"
std_in_chl_string = helper.std_in_chl_file_reader(file_path)
print(std_in_chl_string)
ids_and_elements = parser.parse_std_in_chl_string(std_in_chl_string)

print(topology.find_basic_topology(ids_and_elements=ids_and_elements))