from element import Element
from collections import defaultdict
from typing import Tuple, DefaultDict
import helper

def get_ids_and_elements(std_in_chl_string: str, chemical_formula_start_index: int) -> Tuple[DefaultDict[int, Element], int]:
    
    '''
    we now make all the main elements of the main chain (all elements of the chain excluding hydrogen)
    we extract each of their symbols and instantiate an element class object using the symbol
    '''

    ids_and_elements = defaultdict(Element) # a hashmap that contains the element index as the key, and the element instance as the valu
                                            # this will be useful later

    ith_chemical_formula_index = chemical_formula_start_index # we are now going to iterate through the chemical formula to find the symbols of the main atoms
                                                              # (all atoms excluding hydrogen)

    # iterate until the chemical formula ends in the std in chl string (marked by a forward slash)
    while std_in_chl_string[ith_chemical_formula_index] != '/':
        # if the current character is not hydrogen (since we ignore hydrogen) and its not a digit (since we only look for element symbols)
        if std_in_chl_string[ith_chemical_formula_index] != 'H' and not std_in_chl_string[ith_chemical_formula_index].isdigit():
            symbol_start = ith_chemical_formula_index # element symbols can be multi lettered, so we want to see at which index the element symbol starts and ends
            compound_string_over = False # compound string of the std in chl string can end right after a symbol (eg. C2H6O/, where the slash marks the end, after
                                         # symbol for oxygen O). so this flag says "does the compound string terminate while we iterate to find the symbol"
                                         # false at start
            while not std_in_chl_string[ith_chemical_formula_index].isdigit(): # since symbols are only characters, we iterate until we see a digit
                ith_chemical_formula_index += 1
                if std_in_chl_string[ith_chemical_formula_index] == '/': # if we see a '/' then compound string finished
                    compound_string_over = True # so set the flag to true
                    break # get out of the loop since the chemical formula terminated
            symbol = std_in_chl_string[symbol_start: ith_chemical_formula_index] # splice the symbol from the original string
            
            if symbol not in helper.valency:
                symbol_1 = symbol[:-1]
                symbol_1_element = Element(symbol_1) # create element instance
                ids_and_elements[symbol_1_element.id] = symbol_1_element # this will be useful later
                symbol = symbol[1:]

            if compound_string_over: # if compound string is over without getting to number of elements with that symbol only one element witht that symbol exists
                ith_element = Element(symbol) # create element instance
                ids_and_elements[ith_element.id] = ith_element # this will be useful later
                break

            else: # else we attempt to get the number of elements with that symbol
                number_start = ith_chemical_formula_index # starting index of the number string
                while std_in_chl_string[ith_chemical_formula_index].isdigit(): # we iterate until we see something that is not a digit
                    ith_chemical_formula_index += 1
                
                # get the number of elements by splicing using the indexes we found and converting to int
                number_of_elements = int(std_in_chl_string[number_start: ith_chemical_formula_index])

                # create that many element instances of the symbol
                for i in range(number_of_elements):
                    ith_element = Element(symbol)
                    ids_and_elements[ith_element.id] = ith_element

        else:
            ith_chemical_formula_index += 1 # increment to keep going if the previous cases dont execute
    
    # return element ids and respective element instances along with at which index in the std in chl string the chemical formula section ends for use later
    return ids_and_elements, ith_chemical_formula_index

def set_element_connections_2(connections_string: str, ids_and_elements: DefaultDict[int, Element]) -> None:

    n = len(connections_string)
    if n == 1:
        return
    
    # we always assume i starts at the start of a source id
    # a connection is notated as follows
    # source_element_id(branch_element_id)next_source_element_id
    # or
    # source_element_id-next_source_element_id

    i = 0
    while i < n:
        # first find source_element_id
        if i < n and connections_string[i].isdigit():
            source_element_id_start_index= i
            while i < n and connections_string[i].isdigit():
                i += 1
            source_element_id = int(connections_string[source_element_id_start_index: i])

            '''
            source_element_id(branch_element_id)next_source_element_id...
                             ^
                             |
                             i is currently here

            now, branch_element_id will only exist if there is a branch occuring from the source element
            if there exists no branch from source element it will look like this

            source_element_id-next_source_element_id
                             ^
                             |
                             i is currently here
            
            so after getting source_element_id, connections_string[i] can either be = '-' or '('. lets handle these two cases
            '''

            if i < n and connections_string[i] == '-':
                i += 1
                next_source_element_start_idx = i
                next_source_element_end_idx = i
                while next_source_element_end_idx < n and connections_string[next_source_element_end_idx].isdigit():
                    next_source_element_end_idx += 1
                next_source_element_id = int(connections_string[next_source_element_start_idx: next_source_element_end_idx])
        
                source_element = ids_and_elements[source_element_id]
                next_source_element = ids_and_elements[next_source_element_id]

                source_element.add_connection(next_source_element)
                next_source_element.add_connection(source_element)
            
            elif i < n and connections_string[i] == '(':
                # multiple branches can be notated as (2,3,4)
                # however, each branch can have a connection in and of itself like (2-3,4,5)
                # so we recursively call the set_elements_connections function on all sub connections in the branches
                # sub connections can be defined as the string that comes after a comma or ( and ends before a comma or )
                # we need to end i pointing after the )

                i += 1

                while True:
                    # find branch source id
                    branch_source_start_idx = i
                    while i < n and connections_string[i].isdigit():
                        i += 1
                    branch_source_id = int(connections_string[branch_source_start_idx: i])
                    branch_source = ids_and_elements[branch_source_id]
                    source_element = ids_and_elements[source_element_id]
                    source_element.add_connection(branch_source)
                    branch_source.add_connection(source_element)

                    if connections_string[i] == ',':
                        i += 1
                    else:
                        break

                sub_connection_start_idx = branch_source_start_idx
                j = sub_connection_start_idx
                num_open_brackets = 0
                while True:
                    if j < n and connections_string[j] == '(':
                        num_open_brackets += 1
                    elif j < n and connections_string[j] == ')' and num_open_brackets != 0:
                        num_open_brackets -= 1
                    elif j < n and connections_string[j] == ')' and num_open_brackets == 0:
                        sub_connections_string = connections_string[sub_connection_start_idx: j]
                        # print(sub_connections_string)
                        set_element_connections_2(sub_connections_string, ids_and_elements)
                        i = j + 1
                        break
                    j += 1

                '''
                now,
                source_element_id(branch_element_id)next_source_element_id...
                                                    ^
                                                    |
                                                    i is here
                
                so we need to get next_source_element_id now
                '''

                next_source_element_start_idx = i
                next_source_element_end_idx = i
                while next_source_element_end_idx < n and connections_string[next_source_element_end_idx].isdigit():
                    next_source_element_end_idx += 1
                next_source_element_id = int(connections_string[next_source_element_start_idx: next_source_element_end_idx])
        
                source_element = ids_and_elements[source_element_id]
                next_source_element = ids_and_elements[next_source_element_id]

                source_element.add_connection(next_source_element)
                next_source_element.add_connection(source_element)
        
        else:
            i += 1

def connect_hydrogens_2(std_in_chl_string: str, hydrogen_information_start_index: int, ids_and_elements: DefaultDict[int, Element]) -> None:

    i = hydrogen_information_start_index
    n = len(std_in_chl_string)

    while i < n:
        # some random ahh hydrogen connections that we don't need are notated in brackets
        # we can safely ignore this, and also since these appear at the end of the std_in_chl_string
        # we can break out of the loop if we see a '('
        if std_in_chl_string[i] == '(':
            break
            
        # connection notations for hydrogen end at H
        # 1-4H3 or 1,5,7H
        # we must account for both types of notations

        hydrogen_connection_notation_start_idx = i
        while i < n and std_in_chl_string[i] != 'H':
            i += 1
        hydrogen_connection_notation = std_in_chl_string[hydrogen_connection_notation_start_idx: i]
        
        '''
        1-4H3 or 1,5,7H
           ^          ^
           |          |
        i is here or i is here
        '''

        # now we attempt to get the 'frequency' of H, that is the number written after H
        # if no number is written after H, then frequency = 1
        hydrogen_frequency = 1

        # increment i to now point to the frequency
        i += 1

        if i < n and std_in_chl_string[i].isdigit():
            frequency_start_index = i
            while i < n and std_in_chl_string[i].isdigit():
                i += 1
            hydrogen_frequency = int(std_in_chl_string[frequency_start_index: i])

        # now we process the connection notation string
        # if string contains '-' then it defines a range of numbers (so split with '-' as delimiter)
        # else we split the string with ',' as the delimiter
        j = 0
        m = len(hydrogen_connection_notation)
        import re
        ids = list(map(int, re.split('[,-]', hydrogen_connection_notation)))
        new_ids = set()
        delimeter_count = 0
        visited = set()
        while j < m:
            if hydrogen_connection_notation[j] == ',' or hydrogen_connection_notation[j] == '-':
                delimeter_count += 1
            if hydrogen_connection_notation[j] == ',':
                if ids[delimeter_count - 1] not in visited:
                    new_ids.add(ids[delimeter_count - 1])
            elif hydrogen_connection_notation[j] == '-':
                id_one = ids[delimeter_count - 1]
                id_two = ids[delimeter_count]
                for id in range(id_one, id_two + 1):
                    if id not in visited:
                        new_ids.add(id)
            j += 1
                
        for id in new_ids:
            jth_element = ids_and_elements[id]
            for k in range(hydrogen_frequency):
                ith_hydrogen = Element("H")
                jth_element.add_connection(ith_hydrogen)
                ith_hydrogen.add_connection(jth_element)
        
        # i is now at the comma after H, so let's increment i to ignore the comma
        i += 1

def remove_unnecessary_information(std_in_chl_string: str) -> str:

    # since we dont need information about stereochemistry to make a graph based representation of the compound, we remove it
    # consider InChI=1S/C2H4O2/c3-1-2-4/h1-4H/b2-1+, what you see after /b is the stereochemistry information
    # so we find 'b' and remove from the slash to the left of b until the end of the string
    h_index = std_in_chl_string.find('/h')
    i = h_index + 1
    n = len(std_in_chl_string)

    while i < n and std_in_chl_string[i] != '/':
        i += 1
    
    return std_in_chl_string[0:i]

def parse_std_in_chl_string(std_in_chl_string: str) -> DefaultDict[int, Element]:
    
    std_in_chl_string = remove_unnecessary_information(std_in_chl_string=std_in_chl_string)
    
    # chemical formula (eg: C2H6) starts after the occurence of first '/'
    chemical_formula_start_index = std_in_chl_string.find('/') + 1

    ids_and_elements, chemical_formula_end_index = get_ids_and_elements(std_in_chl_string, chemical_formula_start_index)

    '''
    now, ith_chemical_formula_index is at the slash after the chemical_formula in the std in chl string. so the connections will be notated as
    /c1-2-3 for example
    ^
    |
    ith_chemical_formula_index right now

    we observe that the connections start from two indeces after the slash
    so connections_start_index = ith_chemical_formula_index + 2
    '''
    connections_start_index = chemical_formula_end_index + 2

    # up until the next forward slash, the information about the connections are given
    # so we do
    connections_end_index = std_in_chl_string[connections_start_index:].find('/') + connections_start_index

    connections_string = std_in_chl_string[connections_start_index: connections_end_index]
    set_element_connections_2(connections_string=connections_string, ids_and_elements=ids_and_elements)

    '''
    now, connections_end_index is at the slash after the connections in the std in chl string. so the connections will be notated as
    /h1-4H3 for example
    ^
    |
    ith_chemical_formula_index right now

    we observe that the hydrogen information start from two indeces after the slash
    so hydrogen_information_start_index = connections_end_index + 2
    '''

    hydrogen_information_start_index = connections_end_index + 2
    # connect_hydrogens_2(std_in_chl_string, hydrogen_information_start_index, ids_and_elements)

    helper.print_compound(ids_and_elements)
    Element.next_element_id = 1
    
    return ids_and_elements 