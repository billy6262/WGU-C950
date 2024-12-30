from HashTable import HashTable
class Address:
    def __init__(self, address):
        self.address = address
        self.edges = []

    def __str__(self):
        return f"Address: {self.address} degree {len(self.edges)}"
    

    def degree(self):
        return len(self.edges)
    
    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edges(self):
        return self.edges
    
    def get_sub_addresses(self, addressHashTable ,root = None):
        tempThisEdges = []                                                  
        for edge in self.edges:
            tempThisEdges.append(edge)
        returnAddresses = []
        if root:
            for edge in tempThisEdges:
                if edge.address1 == root or edge.address2 == root:
                    tempThisEdges.remove(edge)
                    break
        if len(tempThisEdges) == 0:
            return [self.address]

        returnAddresses.append(self.address)
        for edge in tempThisEdges:
            if edge.address1 != self.address:
                subAddress = addressHashTable.retrieve(edge.address1)
            elif edge.address2 != self.address:
                subAddress = addressHashTable.retrieve(edge.address2)

            for address in subAddress.get_sub_addresses(addressHashTable, self.address):
                returnAddresses.append(address)
        return returnAddresses
            