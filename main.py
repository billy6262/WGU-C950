import csv
from Package import Package
from HashTable import HashTable
from Edge import Edge

with open('PackageFile.csv', 'r') as csvPackageFile:
    reader = csv.reader(csvPackageFile)
    i = 0  # Counter to skip header rows
    while i < 8:  
        i += 1 
        next(reader)  # Skip header rows

    packageHashTable = HashTable(1000)  # Create a hash table with a size of 1000
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
    distanceHashTable = HashTable(1000)  # Create a hash table with a size of 1000
    for line in reader:
        RowAddress = line[0]
        i = 2
        while i < len(line):
            if line[i] != '':
                edge = Edge( RowAddress, AddressKey[i], line[i])
                distanceHashTable.insert(f"{RowAddress}{AddressKey[i]}", edge)
            else:
                i = 500 # setting an exit condition for the while loop
            i += 1
