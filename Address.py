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
    
    def get_branch(self,addresshashtable, visited=[]): #this function retives all the addreses linked to this address.

        visitedAddresses = visited
        visitedAddresses.append(self.address) #adding current address to the list of visited addreses

        for edge in self.edges:  #if this edge leads to a address not in the list of visited addreses then  recusivly call this function.
            if edge.address1 not in visitedAddresses:
                visitedAddresses = addresshashtable.retrieve(edge.address1).get_branch(addresshashtable, visitedAddresses) #the recursive call is passed a list of visited addreses so it dosnt re visit an address.
                #the value returned by the recursive call includes the list passed it when it was called. by reasigning visitedAddreses to the return you prevent duplicate addresses from being added.
                
            elif edge.address2 not in visitedAddresses:
                visitedAddresses = addresshashtable.retrieve(edge.address2).get_branch(addresshashtable, visitedAddresses)
                


        return visitedAddresses