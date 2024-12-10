import csv
from Package import Package
from HashTable import HashTable

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
