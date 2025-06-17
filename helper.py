from typing import DefaultDict
from element import Element

def std_in_chl_file_reader(path: str) -> str:
    with open(path, 'r') as file:
        return file.readline().strip()

def print_compound(ids_and_elements: DefaultDict[int, Element]) -> None:
    for key in ids_and_elements:
        ids_and_elements[key].print()
        
valency = {
    'H': 1,   # Hydrogen
    'C': 4,   # Carbon
    'N': 3,   # Nitrogen (can be 5 in some cases, but 3 is standard)
    'O': 2,   # Oxygen
    'F': 1,   # Fluorine
    'Cl': 1,  # Chlorine
    'Br': 1,  # Bromine
    'I': 1,   # Iodine
    'S': 2,   # Sulfur (can also be 4 or 6, but 2 is common for organics)
    'P': 3,   # Phosphorus (can be 5 in phosphates, but 3 in organics)
    'B': 3,   # Boron (electron-deficient, common in organics like BF3)
    'Si': 4,  # Silicon (often mirrors carbon)
    'Se': 2,  # Selenium (organic analog of sulfur)
    'Li': 1,  # Lithium (organometallics)
    'Na': 1,  # Sodium
    'K': 1,   # Potassium
    'Mg': 2,  # Magnesium (Grignard reagents)
    'Ca': 2,  # Calcium
    'Zn': 2,  # Zinc (Zn2+ coordination)
    'Al': 3,  # Aluminum
}