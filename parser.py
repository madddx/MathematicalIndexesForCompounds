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

            if compound_string_over: # if compound string is over without getting to number of elements with that symbol only one element witht hat symbol exists
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

def set_element_connections(connections_string: str, ids_and_elements: DefaultDict[int, Element]) -> None:

    n = len(connections_string)
    if n == 1:
        return

    # a connection is notated as follows
    # source_element_id(branch_element_id)next_connection_id-source_element_id...

    # we first find the source
    i = 0
    while i < n:
        # we will first see the source element id
        if connections_string[i].isdigit():
            source_element_id_start_index= i
            while i < n and connections_string[i].isdigit():
                i += 1
            source_element_id = int(connections_string[source_element_id_start_index: i])
            
            '''
            source_element_id(branch_element_id)next_connection_id-source_element_id...
                             ^
                             |
                             i is currently here

            now, branch_element_id and next_connection will only exist if there is a branch occuring from the source element
            if there exists no branch from source element it will look like this

            source_element_id-source_element_id
                             ^
                             |
                             i is currently here
            
            so after getting source_element_id, connections_string[i] can either be = '-' or '('. lets handle these two cases
            '''

            if i < n and connections_string[i] == '-': # that means one source is connected to another source, we get the element id of the next source
                next_source_element_id_start_index = i + 1
                next_source_element_id_digit_index = i + 1
                while next_source_element_id_digit_index < n and connections_string[next_source_element_id_digit_index].isdigit():
                    next_source_element_id_digit_index += 1
                next_source_element_id = int(connections_string[next_source_element_id_start_index: next_source_element_id_digit_index])

                # now that we have obtained the next element source id, we append next_source_element_id as a connecton of source_element,
                # and source_element_id as a connection of next_source_element

                source_element = ids_and_elements[source_element_id]
                next_source_element = ids_and_elements[next_source_element_id]

                source_element.add_connection(next_source_element)
                next_source_element.add_connection(source_element)

            elif i < n and connections_string[i] == '(':
                # multiple branches can be notated as (2,3,4)
                # however, each branch can have a connection and and of itself like (2-3,4,5)
                # so we recursively call the set_elements_connections function on all sub connections in the branches
                # sub connections can be defined as the string that comes after a comma or ( and ends before a comma or )
                # we need to end i pointing at the )

                while connections_string[i] != ')':
                    if connections_string[i] == '(' or connections_string[i] == ',': # we found a sub connection
                        i += 1
                        sub_connection_start_index = i
                        # we first need to find the source of the sub connection (first element id that appears in the sub connection)
                        while connections_string[i].isdigit():
                            i += 1
                        sub_connection_source_element_id = int(connections_string[sub_connection_start_index: i])
                        source_element = ids_and_elements[source_element_id]
                        sub_connection_source_element = ids_and_elements[sub_connection_source_element_id]

                        source_element.add_connection(sub_connection_source_element)
                        sub_connection_source_element.add_connection(source_element)

                        # now we get the sub connection as a whole and send it to set elements function
                        while connections_string[i] != ')' and connections_string[i] != ',':
                            i += 1
                        sub_connections_string = connections_string[sub_connection_start_index: i]
                        set_element_connections(sub_connections_string, ids_and_elements)
                        
                    else:
                        i += 1

                '''
                now,
                source_element_id(branch_element_id)next_connection_id-source_element_id...
                                                   ^
                                                   |
                                                   i is here
                
                so we need to get next_connection_id now
                '''

                # increment i to go to the start of the next connection id
                i += 1
                next_connection_id_start = i
                while i < n and connections_string[i].isdigit():
                    i += 1
                next_connection_id = int(connections_string[next_connection_id_start: i])

                # we connect both elements now
                source_element = ids_and_elements[source_element_id]
                next_connection = ids_and_elements[next_connection_id]

                source_element.add_connection(next_connection)
                next_connection.add_connection(source_element)

                '''
                now, we are at the '-' before the next source element
                source_element_id(branch_element_id)next_connection_id-source_element_id...
                                                                      ^
                                                                      |
                                                                      i is here
                '''

                if i < n and connections_string[i] == '-':
                    next_source_element_id_start_index = i + 1
                    next_source_element_id_digit_index = i + 1
                    while next_source_element_id_digit_index < n and connections_string[next_source_element_id_digit_index].isdigit():
                        next_source_element_id_digit_index += 1
                    next_source_element_id = int(connections_string[next_source_element_id_start_index: next_source_element_id_digit_index])

                    next_source_element = ids_and_elements[next_connection_id]

                    next_connection.add_connection(next_source_element)
                    next_source_element.add_connection(next_connection)
        else:
            i += 1

def connect_hydrogens(std_in_chl_string: str, hydrogen_information_start_index: int, ids_and_elements: DefaultDict[int, Element]) -> None:

    i = hydrogen_information_start_index
    n = len(std_in_chl_string)
    while i < n:
        # we found the element ids to which hydrogen is attached
        if std_in_chl_string[i].isdigit():
            # the ids can be notated as such: 1-4, so we need to find from_element_id and to_element_id
            from_element_id_start_index = i
            to_element_id_start_index = -1
            while i < n and std_in_chl_string[i].isdigit():
                i += 1
            
            from_element_id = int(std_in_chl_string[from_element_id_start_index: i])

            if i < n and std_in_chl_string[i] == '-':
                i += 1
                to_element_id_start_index = i
                while i < n and std_in_chl_string[i].isdigit():
                    i += 1

                to_element_id = int(std_in_chl_string[to_element_id_start_index: i])

            '''
            1-4H3
               ^
               |
               i is here

            we need the frequency of hydrogen which is located next to where i is located. so increment i
            '''

            i += 1
            frequency_start_index = i
            while i < n and std_in_chl_string[i].isdigit():
                i += 1

            frequency = int(std_in_chl_string[frequency_start_index: i]) if len(std_in_chl_string[frequency_start_index: i]) > 0 else 1
            
            # if we only have a from element id
            if to_element_id_start_index == -1:
                from_element = ids_and_elements[from_element_id]
                for _ in range(frequency):
                    ith_hydrogen = Element("H")
                    from_element.add_connection(ith_hydrogen)
                    ith_hydrogen.add_connection(from_element)

            # if we have both from element id and to element id
            else:
                for ith_element_id in range(from_element_id, to_element_id + 1):
                    ith_element = ids_and_elements[ith_element_id]
                    for _ in range(frequency):
                        _th_hydrogen = Element("H")
                        ith_element.add_connection(_th_hydrogen)
                        _th_hydrogen.add_connection(ith_element)

        else:
            i += 1

def remove_stereochemistry_information(std_in_chl_string: str) -> str:

    # since we dont need information about stereochemistry to make a graph based representation of the compound, we remove it
    # consider InChI=1S/C2H4O2/c3-1-2-4/h1-4H/b2-1+, what you see after /b is the stereochemistry information
    # so we find 'b' and remove from the slash to the left of b until the end of the string
    b_index = std_in_chl_string.find('b')
    
    if b_index == -1:
        return std_in_chl_string
    else:
        return std_in_chl_string[0: b_index - 1]

# function to add double bonds and triple bonds (by fulfilling valency of each element)
# dont dwell on this too much
def materialize_double_and_triple_bonds(ids_and_elements: DefaultDict[int, Element]) -> None:

    for key in ids_and_elements:
        ith_element = ids_and_elements[key]
        for connection in ith_element.connections:
            effective_valency = connection.valency - connection.get_num_connections()
            for _ in range(effective_valency):
                ith_element.add_connection(connection)
                connection.add_connection(ith_element)


def parse_std_in_chl_string(std_in_chl_string: str) -> DefaultDict[int, Element]:
    
    std_in_chl_string = remove_stereochemistry_information(std_in_chl_string=std_in_chl_string)

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
    set_element_connections(connections_string=connections_string, ids_and_elements=ids_and_elements)

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
    connect_hydrogens(std_in_chl_string, hydrogen_information_start_index, ids_and_elements)

    materialize_double_and_triple_bonds(ids_and_elements=ids_and_elements)

    helper.print_compound(ids_and_elements)

    return ids_and_elements