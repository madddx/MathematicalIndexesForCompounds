from typing import DefaultDict
from element import Element

def std_in_chl_file_reader(path: str) -> str:
    with open(path, 'r') as file:
        return file.readline().strip()

def print_compound(ids_and_elements: DefaultDict[int, Element]) -> None:
    for key in ids_and_elements:
        ids_and_elements[key].print()