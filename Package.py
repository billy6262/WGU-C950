import datetime


class Package:
    def __init__(self, ID , address, city, state, zip, deliveryDeadLine, weight, notes):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadLine = deliveryDeadLine
        self.weight = weight
        self.status = [["At hub", datetime.time(8)]]
        self.deliveryTime = None
        self.notes = notes
    

    def __str__(self):
        return f'Package ID: {self.ID} Address: {self.address} City: {self.city} State: {self.state} Zip: {self.zip} Delivery Status:{self.status[len(self.status)-1][0]} Time: {self.status[len(self.status) - 1][1]}'
    

    def status_update(self, time, status):
        self.status.append([status, time])

    def get_status(self):
        return f'ID: {self.ID}   Address: {self.address}   {self.status[len(self.status)-1][0]} {self.status[len(self.status)-1][1]}'