import csv
from Package import Package
from HashTable import HashTable
from Edge import Edge
from Truck import Truck
from Address import Address

with open('PackageFile.csv', 'r') as csvPackageFile:
    reader = csv.reader(csvPackageFile)
    i = 0  # Counter to skip header rows
    while i < 8:  
        i += 1 
        next(reader)  # Skip header rows

    packageHashTable = HashTable(100)  # Create a hash table with a size of 1000 to store the package information
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
                distanceHashTable.insert(f"{RowAddress}{AddressKey[i]}", edge) #hashing diatance table based off of the 2 relavent addresses
            else:
                i = 500 # setting an exit condition for the while loop
            i += 1
    csvDistanceFile.close()


truck1 = Truck(18, [20,21,16,34,19,13,39,14,15], 0, AddressKey[2],0)
truck2 = Truck(18, [3,5,17,19,36,37,28], 0, AddressKey[2],0)
truck3 = Truck(18, [6,9,8,25,26,28,32], 0, AddressKey[2],0)

together = [20,21,16,34,19,13,39,14,15] # 6 aadresses
#rush [7,29,1,8,30,31,4,40,5,37] 5 addresses
#delayed on flight and rushed [28,6,32,25,26]
#truck2 [18,36,3,38,9]  id 9 is delayed address
#all other [27,35,2,33,11,17,12,24,23,10,22]


def calculate_route(packages):
    #this section retives the addresses and associated edges for the packages

    addressHashTable = HashTable(25) #this table will store the address just for this route  
    addressHashTable.insert(AddressKey[2],Address(AddressKey[2])) #inserting the address of the depot where all routes start
    addresses = [AddressKey[2]]             #a address list is needed to be able to iterate over it
    routEdges = []                          #edges between all addresses will be stored in this list enabeling it to be sorted by length.
    for id in packages:                     #retriving package information from the package hash table
        package = packageHashTable.retrieve(id)
        if package.address not in addresses:
            addresses.append(package.address)
            addressHashTable.insert(package.address,Address(package.address))

    for addressP in addresses:          #reforming a distance table for just the addreses of the packages are added
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
        subAddresses = addFrom.get_sub_addresses(addressHashTable)  #this function recusivly retives all addreses connected to the address is is called from.
        if addFrom.degree() == 0 or addTo.degree() == 0:  #if the address is not conected or has a degree 0 then it can be conected without forming a loop
            addFrom.add_edge(edge)
            addTo.add_edge(edge)
        elif addTo.address not in subAddresses:  #by checking the address agains all addresses ion the tree it will be conected to we can varifiy if it will form a loop.
            addFrom.add_edge(edge)
            addTo.add_edge(edge)
    

    #this section turns the tree into a eulerian path

    oddDegreeAddresses = []
    oddDegreeRoutEdges = []
    for address in addresses:
        if addressHashTable.retrieve(address).degree() % 2!= 0:
            oddDegreeAddresses.append(address)

    for addressP in oddDegreeAddresses:          #reforming a distance table for just the addreses of odd degree
        for addressS in oddDegreeAddresses:
            edge = distanceHashTable.retrieve_distances(addressP,addressS)
            if edge:                    #if the distance is found, it is added to the routEdges table
                oddDegreeRoutEdges.append(edge)  #adding distances for just odd degree addreses to a new list
    oddDegreeRoutEdges = list(set(oddDegreeRoutEdges)) # removing duplicates
    oddDegreeRoutEdges.sort(key=lambda e: e.ilength)  #sorting the edges from shortest to longest
    for edge in oddDegreeRoutEdges:
        if addressHashTable.retrieve(edge.address1).address in oddDegreeAddresses and addressHashTable.retrieve(edge.address2).address in oddDegreeAddresses:
            addFrom = addressHashTable.retrieve(edge.address1)
            addTo = addressHashTable.retrieve(edge.address2)
            addFrom.add_edge(edge)
            addTo.add_edge(edge)
            oddDegreeAddresses.remove(addFrom.address)
            oddDegreeAddresses.remove(addTo.address)


    #this section will take each edge and if it is to a address already visited replace it with a edge from the current address to the next unvisited address.

    visitedAddresses = []
    for address in addressHashTable.retrieve(AddressKey[2]).traverse(addressHashTable):
        if address not in visitedAddresses:
            visitedAddresses.append(address)
            print(address)




    


calculate_route(together)

