#Western Governors University Parcel Service (WGUPS) WGU Student ID: 004855809
#-----------------------------------------------
#designed by Andrew M Dorchak
#-----------------------------------------------
#An implamentation of the Christofides–Serdyukov algorithm

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
    distanceHashTable = HashTable(2000)  # Create a hash table with a size of 1000 to store the distance
    for line in reader:
        RowAddress = line[1]
        i = 2
        while i < len(line):
            if line[i] != ''  and line[i] != '0':
                edge = Edge( RowAddress, AddressKey[i], line[i])
                distanceHashTable.insert(f"{AddressKey[i]}{RowAddress}", edge) #hashing distance table based off of the 2 relevant addresses
            else:
                i = 500 # setting an exit condition for the while loop
            i += 1
    csvDistanceFile.close()


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
    


    #this section makes a minimum spanning tree(MST) with the addreses accociated with our packages.
    #it dose this by systamaticaly selecting the shortest edge that dose not create a loop till all nodes are connected.
    
    for edge in routEdges:
        addFrom = addressHashTable.retrieve(edge.address1)
        addTo = addressHashTable.retrieve(edge.address2)

        if addFrom.degree() == 0 or addTo.degree() == 0:  #if the address is not connected or has a degree 0 then it can be connected without forming a loop
            addFrom.add_edge(edge)
            addTo.add_edge(edge)
            continue
        subAddresses = addFrom.get_branch(addressHashTable, [addFrom.address])  #this function recursively retrieves all addresses connected to the address it is called from.
        if addTo.address not in subAddresses:  #by checking the address against all addresses in the tree it will be connected to we can verify if it will form a loop.
            addFrom.add_edge(edge)
            addTo.add_edge(edge)




    #this section turns the MST into a eulerian cycle.
    #this section of code implments what is called a perfect pairing.
    #the nodes with an odd number of edges are connected by a new edge.
    #there is always an even number of nodes with odd edges so by doing this we ensure that all nodes now have an even dgree.
    #this makes it posible to traverse the graph in an eularian cycle by altering out MST. 

    oddDegreeAddresses = []
    oddDegreeRoutEdges = []
    for address in addresses:
        if addressHashTable.retrieve(address).degree() % 2!= 0:        #compiling a list of nodes in the MST with an odd degree.
            oddDegreeAddresses.append(address)

    for addressP in oddDegreeAddresses:          #reforming a distance table for just the addresses of odd degree
        for addressS in oddDegreeAddresses:
            edge = distanceHashTable.retrieve_distances(addressP,addressS)
            if edge:                    #if the distance is found, it is added to the Edges table
                oddDegreeRoutEdges.append(edge)  #adding distances for just odd degree addresses to a new list
    oddDegreeRoutEdges = list(set(oddDegreeRoutEdges)) # removing duplicates
    oddDegreeRoutEdges.sort(key=lambda e: e.ilength)  #sorting the edges from shortest to longest
    for edge in oddDegreeRoutEdges:                   #taking the shorest edge first and connecting it to to nodes that have an odd degree.
        if edge.address1 in oddDegreeAddresses and edge.address2 in oddDegreeAddresses:  
            addFrom = addressHashTable.retrieve(edge.address1)                       
            addTo = addressHashTable.retrieve(edge.address2)                      
            addFrom.add_edge(edge)                                        #adding the edge to each node.          
            addTo.add_edge(edge)
            oddDegreeAddresses.remove(addFrom.address)
            oddDegreeAddresses.remove(addTo.address)        #now that the 2 nodes now have an even degree they are removed from the list so they will not be evaluated again.

    #now that we have a eularian cycle we will traverse the nodes in order and record that order with this function.
    #this gives us an ordered list of nodes representing the eularian cycle.

    def traverse_addreses(thisaddress,  caller = None): #traverse returns a list of all addresses in this tree in the order they would be traversed in a eularian cycle
        returnAddreses = []            
        returnAddreses.append(thisaddress.address)

        for edge in thisaddress.edges:                #if this function is called recursively then the edge connecting it to the caller address will be removed to prevent the function from back tracking.
            if edge.address1 == caller or edge.address2 == caller:
                thisaddress.edges.remove(edge)                 
                break                                 
        
        if len(thisaddress.edges) == 3: #checking that i dont sever a branch and leave it un attached. this is a pitfall that ocure when encountering self contained loops
            if thisaddress.edges[0].address1 == thisaddress.address:
                subadd = addressHashTable.retrieve(thisaddress.edges[0].address2).get_branch(addressHashTable,[thisaddress.address]) #this retrives all sub addresses for this branch
                if not(thisaddress.edges[2].address1 in subadd and thisaddress.edges[2].address2 in subadd): #comparing the subaddreses with the other edges in this node to evaluate wivh edge to traverse to prevbent severingthe loop.
                    thisaddress.edges.append(thisaddress.edges[0])
                    thisaddress.edges.pop(0)


        if len(thisaddress.edges) > 0:       #check to see if this address has any edges
            if caller in [thisaddress.edges[0].address1,thisaddress.edges[0].address2]: #if possible prefer edges that dont return to the last address. this prevents svering a loop.
                thisaddress.edges.append(thisaddress.edges[0])                                                                          
                thisaddress.edges.pop(0)   #re-ordering the edges so as to not return to the last address

            if thisaddress.edges[0].address1 == thisaddress.address:  #checking the correct direction to traverse on the edge.
                addressOut = str(thisaddress.edges[0].address2 + "")
            else:
                addressOut = str(thisaddress.edges[0].address1 + "")  #checking the correct direction to traverse on the edge.

            thisaddress.edges.pop(0) #removing the edge about to be traversed 



            for address in traverse_addreses(addressHashTable.retrieve(addressOut),thisaddress.address): #traversing the first edge in the address object to the adjacent address and recursively calling traverse
                returnAddreses.append(address)              #appending the edges traversed in the recursive calls to the list to be returned.

        return returnAddreses  

    #once we have traversed the graph we will take our ordered list of addresses and skip any address that is repeated. 
    #this is the equivilent of skipping any intermidiate address that has been visited and going directly to the next new address.
    #by doing this we are changing our eularian cycle into a hamiltonian cycle where each node is visited exactly once.

    finalRoute = []
    traversedUlar = traverse_addreses(addressHashTable.retrieve(AddressKey[2]))

    for address in traversedUlar:
        if address not in finalRoute:
            finalRoute.append(address)   #removing any backtracking turning it from a eularian cycle to a hamiltonian path.
    return finalRoute
 



# package loads for each truck.composition is based on delivery window and requierments.
rush = [7,29,1,8,30,4,40,5,37,17,2,33] 
together = [20,21,16,34,19,13,39,14,15,11,23,18,36,3,38] 
delayed = [28,6,32,31,25,26,27,35,10,24,27,22,12,9]

truck1 = Truck("Truck 1 trip 1",18, rush, 0, AddressKey[2],packageHashTable,calculate_route(rush))
truck1.drive_route(distanceHashTable)

#load truck 2 with the "together" packages and dispatch the truck.
truck2 = Truck("Truck 2 trip 1",18, together, 0, AddressKey[2],packageHashTable,calculate_route(together))
truck2.drive_route(distanceHashTable)

#load truck 1 with the "delayed" packages and dispatch the truck.
truck1 = Truck("Truck 1 trip 2",18, delayed, truck1.mileage, AddressKey[2],packageHashTable,calculate_route(delayed),truck1.currentTime)
truck1.drive_route(distanceHashTable)


#preamble to user interface.
print("Western Governors University Parcel Service (WGUPS)")
print("-----------------------------------------------")
print("designed by Andrew M Dorchak")
print("WGU Student ID: 004855809")
print("-----------------------------------------------")
print("total milage traveled:")
print(f"Truck 1 {truck1.mileage} miles   Truck 2 {truck2.mileage} miles.")
print(f"Total miles between all trucks traveled: {truck1.mileage + truck2.mileage} miles.")
print("-----------------------------------------------")
print("Time each truck returned to the depot for the end of the day.")
print(f"Truck 1 {truck1.currentTime}    Truck 2 {truck2.currentTime}")


while True: #input loop. only way to exit is to enter E.
    INPUT =  input("To view a specific package enter ID. To view the status of all packages at a certain time enter ALL. For the en route report enter REPORT or enter E to exit.") #grabing a input for the type of request.
    if INPUT.upper() == "ALL": 
        try: #using try to catch any data entry error
            INPUT = input("Enter a time in format HH:MM")
            (H,M) = INPUT.split(":") #seperating the value for the hour and minute fields.
            i = 1
            while i <= 40: #itterating over the package ids 
                package = packageHashTable.retrieve(i) #reteriving the package object
                print(package.get_status_by_time(datetime.timedelta(hours=int(H), minutes= int(M)))) #calling a function that returns the package status at that time as a string.
                i += 1

        except ValueError:
            print("Invalid time format. Please enter a time in format HH:MM")  #catching data entry errors
            continue
    elif INPUT.upper() == "ID":
        try: #using try to catch any data entry error
            INPUT = int(input("Enter package ID: ")) #grabing the ID of the package to be viewed
            package = packageHashTable.retrieve(INPUT)  #retriving the package object
            print(package) #print package info
        
        except KeyError: # 
            print("Package not found.") #catching data entry errors
            continue

    elif INPUT.upper() == "REPORT":
        print()
        print("En route report for 08:35 a.m.:")
        i = 1
        while i <= 40: #itterating over the package ids
            package = packageHashTable.retrieve(i) #reteriving the package object
            if package.status[1][1] < datetime.timedelta(hours=8,minutes=35) and package.status[2][1] >  datetime.timedelta(hours=8,minutes=35):
                print(f"ID: {package.ID}  Address: {package.get_address(datetime.timedelta(hours=8,minutes=35))}  Package Status: {package.status[1][0]}  last updated at: {package.status[1][1]} Delivery Deadline: {package.deliveryDeadLine}")
            i += 1
        print()
        print("En route report for 09:35 a.m.:")
        i = 1
        while i <= 40: #itterating over the package ids
            package = packageHashTable.retrieve(i) #reteriving the package object
            if package.status[1][1] < datetime.timedelta(hours=9,minutes=35) and package.status[2][1] >  datetime.timedelta(hours=9,minutes=35):
                print(f"ID: {package.ID}  Address: {package.get_address(datetime.timedelta(hours=9,minutes=35))}  Package Status: {package.status[1][0]}  last updated at: {package.status[1][1]} Delivery Deadline: {package.deliveryDeadLine}")
            i += 1
        print()
        print("En route report for 12:03 a.m.:")
        i = 1
        while i <= 40: #itterating over the package ids
            package = packageHashTable.retrieve(i) #reteriving the package object
            if package.status[1][1] < datetime.timedelta(hours=12,minutes=3) and package.status[2][1] >  datetime.timedelta(hours=12,minutes=3): 
                print(f"ID: {package.ID}  Address: {package.get_address(datetime.timedelta(hours=12,minutes=3))}  Package Status: {package.status[1][0]}  last updated at: {package.status[1][1]} Delivery Deadline: {package.deliveryDeadLine}")
            i += 1


    elif INPUT.upper() == "E": #exit the program
        exit()


