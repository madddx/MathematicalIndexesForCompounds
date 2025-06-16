import helper
import parser

file_path = r"D:\Education\Code Bases\Python\StdInChlParser\std_in_chl_string2.text"
std_in_chl_string = helper.std_in_chl_file_reader(file_path)
print(std_in_chl_string)
parser.parse_std_in_chl_string(std_in_chl_string)