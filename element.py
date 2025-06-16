from __future__ import annotations

class Element:

    next_element_id = 1

    def __init__(self, symbol: str):
        
        self.id = Element.next_element_id
        Element.next_element_id += 1
        self.symbol = symbol
        self.connections = []

    def add_connection(self, element: Element) -> None:
        self.connections.append(element)
    
    def print(self) -> None:
        print(self.symbol, ":", self.id, end=" ")
        print("[", end=" ")
        for connection in self.connections:
            print(connection.symbol, ":", connection.id, ",", end=" ")
        print("]")