import datetime


class Truck:
    def __init__(self,name ,speed,packages, mileage, currentAdress, packageHashTable, route = None):
        self.name = name
        self.speed = speed
        self.mileage = mileage
        self.currentAdress = currentAdress
        self.currentTime = datetime.timedelta(hours=8)
        self.route = route
        self.packageTable = []

        for packageid in packages: # packages are passed as a list of IDs. this is retriving the objects.
            self.packageTable.append(packageHashTable.retrieve(packageid))

    def new_route_and_packages(self, route, packages,packageHashTable):
        self.route = route
        self.packages = packages
        for packageid in packages: # packages are passed as a list of IDs. this is retriving the objects.
            self.packageTable.append(packageHashTable.retrieve(packageid))

    def drive_route(self, distanceHashTable):
        
        for package in self.packageTable:
            package.status_update(self.currentTime,f"Enroute on {self.name}.") #update the status of the package to be enroute

        for address in self.route:
            if address == "4001 South 700 East":        #seting the start location
                self.currentAdress = address
            else:
                edge = distanceHashTable.retrieve_distances(self.currentAdress, address)
                self.currentAdress = address
                self.mileage = self.mileage + float(edge.length)
                self.currentTime += datetime.timedelta(hours=float(edge.length)/float(self.speed))
                for package in self.packageTable:       #unloading all the packages for that address
                    if package.address == self.currentAdress:
                        package.status_update(self.currentTime,f"Delivered by {self.name}.")

        edge = distanceHashTable.retrieve_distances(self.currentAdress,"4001 South 700 East") #returning to the depot
        self.currentAdress = "4001 South 700 East"
        self.mileage = self.mileage + float(edge.length)
        self.currentTime += datetime.timedelta(hours=float(edge.length)/float(self.speed))

        return self.mileage


    