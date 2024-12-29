from HashTable import HashTable
class Address:
    def __init__(self, address):
        self.address = address
        self.edges = []

    def __str__(self):
        return f"Address: {self.address}"
    
    def traverse(self,addressHashTable, caller = None):       #traverse returns a list of all addresses in this tree in the order they would be travered in a hamiltonian circuit
        returnAddreses = []
        returnAddreses.append(self.address)

        for edge in self.edges:                #if this function is called recursivly then the edge conecting it to the caller address will be removed to prevent the function from back tracking.
            if edge.address1 == caller or edge.address2 == caller:
                self.edges.remove(edge)                 
                break                                 


        if len(self.edges) > 0:       #check to see if this address has any edges
            if self.edges[0].address1 == self.address:  #checking the correct dirtection to traverse on the edge.
                addressOut = str(self.edges[0].address2 + "")
            else:
                addressOut = str(self.edges[0].address1 + "")  #checking the correct dirtection to traverse on the edge.
            self.edges.pop(0) #removing the edge about to be traversed 



            for edge in addressHashTable.retrieve(addressOut).traverse(addressHashTable,self.address):               #traversing the first edge in the address object to the adjacent address and recursivly calling traverse
                returnAddreses.append(edge)              #appending the edges traversed in the recursive calls to the list to be returned.
            

        return returnAddreses  


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
            