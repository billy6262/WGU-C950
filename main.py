import csv
import datetime
from Package import Package
from HashTable import HashTable
from Edge import Edge
from Truck import Truck
from Address import Address

#these sections import the data from the CSV files
with open('PackageFile.csv', 'r') as csvPackageFile:
    reader = csv.reader(csvPackageFile)
    i = 0  # Counter to skip header rows
    while i < 5:  
        i += 1 
        next(reader)  # Skip header rows

    packageHashTable = HashTable(1000)  # Create a hash table with a size of 1000 to store the package information
    for line in reader:
        package = Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])
        packageHashTable.insert(package.ID, package)


with open('DistanceFile.csv', 'r') as csvDistanceFile:
    reader = csv.reader(csvDistanceFile)
    i = 0 # Counter to skip header rows
    while i < 7:
        i += 1
        next(reader)  # Skip header rows
    AddressKey = next(reader) #first column is at index 2 on row 6
    distanceHashTable = HashTable(1000)  # Create a hash table with a size of 1000 to store the distance
    for line in reader:
        RowAddress = line[1]
        i = 2
        while i < len(line):
            if line[i] != ''  and line[i] != '0':
                edge = Edge( RowAddress, AddressKey[i], line[i])
                distanceHashTable.insert(f"{RowAddress}{AddressKey[i]}", edge) #hashing distance table based off of the 2 relevant addresses
            else:
                i = 500 # setting an exit condition for the while loop
            i += 1
    csvDistanceFile.close()


together = [20,21,16,34,19,13,39,14,15,2,33,17,11,23,22] 
rush = [7,29,1,8,30,31,4,40,5,37] 
delayed = [28,6,32,25,26,27,35,10,24]
truck2p = [18,36,3,38,9,27]


def calculate_route(packages):
    #this section retrieves the addresses and associated edges for the packages

    addressHashTable = HashTable(1000) #this table will store the address just for this route  
    addressHashTable.insert(AddressKey[2],Address(AddressKey[2])) #inserting the address of the depot where all routes start
    addresses = [AddressKey[2]]             #a address list is needed to be able to iterate over it
    routEdges = []                          #edges between all addresses will be stored in this list enabling it to be sorted by length.
    for id in packages:                     #retrieving package information from the package hash table
        package = packageHashTable.retrieve(id)
        if package.address not in addresses:
            addresses.append(package.address)
            addressOBJ = Address(package.address)
            addressHashTable.insert(package.address,addressOBJ)

    for addressP in addresses:          #reforming a distance table for just the addresses of the packages are added
        for addressS in addresses:
            edge = distanceHashTable.retrieve_distances(addressP,addressS)
            if edge:                    #if the distance is found, it is added to the routEdges table
                routEdges.append(edge)  #adding distances for just this rout to a new list
    routEdges = list(set(routEdges)) # removing duplicates
    routEdges.sort(key=lambda e: e.ilength)  #sorting the edges from shortest to longest
    
    #this section makes a minimum spanning tree
    
    for edge in routEdges:
        addFrom = addressHashTable.retrieve(edge.address1)
        addTo = addressHashTable.retrieve(edge.address2)
        subAddresses = addFrom.get_sub_addresses(addressHashTable)  #this function recursively retrieves all addresses connected to the address it is called from.
        if addFrom.degree() == 0 or addTo.degree() == 0:  #if the address is not connected or has a degree 0 then it can be connected without forming a loop
            addFrom.add_edge(edge)
            addTo.add_edge(edge)

        elif addTo.address not in subAddresses:  #by checking the address against all addresses in the tree it will be connected to we can verify if it will form a loop.
            addFrom.add_edge(edge)
            addTo.add_edge(edge)




    #this section turns the tree into a eulerian path 

    oddDegreeAddresses = []
    oddDegreeRoutEdges = []
    for address in addresses:
        if addressHashTable.retrieve(address).degree() % 2!= 0:
            oddDegreeAddresses.append(address)

    for addressP in oddDegreeAddresses:          #reforming a distance table for just the addresses of odd degree
        for addressS in oddDegreeAddresses:
            edge = distanceHashTable.retrieve_distances(addressP,addressS)
            if edge:                    #if the distance is found, it is added to the routEdges table
                oddDegreeRoutEdges.append(edge)  #adding distances for just odd degree addresses to a new list
    oddDegreeRoutEdges = list(set(oddDegreeRoutEdges)) # removing duplicates
    oddDegreeRoutEdges.sort(key=lambda e: e.ilength)  #sorting the edges from shortest to longest
    for edge in oddDegreeRoutEdges:
        if edge.address1 in oddDegreeAddresses and edge.address2 in oddDegreeAddresses:
            addFrom = addressHashTable.retrieve(edge.address1)
            addTo = addressHashTable.retrieve(edge.address2)
            addFrom.add_edge(edge)
            addTo.add_edge(edge)
            oddDegreeAddresses.remove(addFrom.address)
            oddDegreeAddresses.remove(addTo.address)



    def traverse_addreses(thisaddress,  caller = None): #traverse returns a list of all addresses in this tree in the order they would be traversed in a eularian circuit
        returnAddreses = []            
        returnAddreses.append(thisaddress.address)
        if caller == None:                                                  #if you dont remove an edge from the address you start at you could cause a deadlock.
            if thisaddress.edges[0].address1 == thisaddress.address:          
                addressOut = str(thisaddress.edges[0].address2 + "")
            else:
                addressOut = str(thisaddress.edges[0].address1 + "")
            
            addressHashTable.retrieve(addressOut).edges.remove(distanceHashTable.retrieve_distances(addressOut, thisaddress.address)) #removing the coresponding edge in the other address
            thisaddress.edges.pop(0)


        for edge in thisaddress.edges:                #if this function is called recursively then the edge connecting it to the caller address will be removed to prevent the function from back tracking.
            if edge.address1 == caller or edge.address2 == caller:
                thisaddress.edges.remove(edge)                 
                break                                 
        
        if len(thisaddress.edges) == 3: #checking that i dont sever a branch and leave it un attached.
            if thisaddress.edges[1] == thisaddress.edges[2] or caller in [thisaddress.edges[0].address1,thisaddress.edges[0].address2]: #if there is a 2 way edge take that edge first
                thisaddress.edges.append(thisaddress.edges[0])                                                                          #if possible prefer edges that dont return to the last address
                thisaddress.edges.pop(0)   #re-ordering the edges so as to not return to the last address

        if len(thisaddress.edges) > 0:       #check to see if this address has any edges
            if thisaddress.edges[0].address1 == thisaddress.address:  #checking the correct direction to traverse on the edge.
                addressOut = str(thisaddress.edges[0].address2 + "")
            else:
                addressOut = str(thisaddress.edges[0].address1 + "")  #checking the correct direction to traverse on the edge.
            print(thisaddress.edges[0])
            thisaddress.edges.pop(0) #removing the edge about to be traversed 



            for address in traverse_addreses(addressHashTable.retrieve(addressOut),thisaddress.address): #traversing the first edge in the address object to the adjacent address and recursively calling traverse
                returnAddreses.append(address)              #appending the edges traversed in the recursive calls to the list to be returned.

        return returnAddreses  



    #for edge in addressHashTable.retrieve(addresses[]).edges:

    finalRoute = []
    x = traverse_addreses(addressHashTable.retrieve(AddressKey[2]))

    for address in x:
        if address not in finalRoute:
            finalRoute.append(address)   #removing any backtracking turning it from a eularian cycle to a hamiltonian path

    for address in addresses:
        print(address)

    print(len(addresses))
    print(len(finalRoute))
    return finalRoute
 

#load truck 1 with the "rush" packages and dispatch the truck.
truck1 = Truck("Truck 1",18, rush, 0, AddressKey[2],packageHashTable,calculate_route(rush))
print(truck1.drive_route(distanceHashTable))

#load truck 2 with the "together" packages and dispatch the truck.
truck2 = Truck("Truck 2",18, together, 0, AddressKey[2],packageHashTable,calculate_route(together))
print(truck2.drive_route(distanceHashTable))

#load truck 1 with the "delayed" packages and dispatch the truck.
truck1.new_route_and_packages(calculate_route(delayed),delayed,packageHashTable)
print(truck1.drive_route(distanceHashTable))

#load truck 2 with the "truck2p" packages and dispatch the truck.
truck2.new_route_and_packages(calculate_route(truck2p),truck2p,packageHashTable)
print(truck2.drive_route(distanceHashTable))






