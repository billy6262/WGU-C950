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
    
    def get_sub_addresses(self, addressHashTable ,root = None): #this function returns all addreses attached to this address
        tempThisEdges = list(self.edges)
        returnAddresses = []
        if root:        #removing the edge this function was called from
            for edge in tempThisEdges:
                if edge.address1 == root or edge.address2 == root:
                    tempThisEdges.remove(edge)
                    break

        returnAddresses.append(self.address) #adding this address to the return list

        for edge in tempThisEdges:
            if edge.address1 != self.address:
                subAddress = addressHashTable.retrieve(edge.address1) #recursivly calleing this function to retive sub addresses
            elif edge.address2 != self.address:
                subAddress = addressHashTable.retrieve(edge.address2)

            returnAddresses.extend(subAddress.get_sub_addresses(addressHashTable, self.address)) #adding the addreses from recursiv calls to the return
                
        return returnAddresses
            