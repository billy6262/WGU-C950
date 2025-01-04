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
        self.status = [["At hub", datetime.timedelta(hours=8)]]
        self.deliveryTime = None
        self.notes = notes
    

    def __str__(self):
        return f'Package ID: {self.ID} Address: {self.address} Delivery Deadline: {self.deliveryDeadLine} City: {self.city} Zip: {self.zip} Weight: {self.weight} Delivery Status:{self.status[len(self.status)-1][0]} Time: {self.status[len(self.status) - 1][1]}'
    

    def status_update(self, time, status):
        self.status.append([status, time])

    def get_status(self):
        return f'ID: {self.ID}   Address: {self.address}   {self.status[len(self.status)-1][0]} {self.status[len(self.status)-1][1]}  Delivery Deadline: {self.deliveryDeadLine}'
    
    def get_status_by_time(self, time):
        Rlist = []
        for status in self.status:
            if status[1] < time:
                Rlist.append(status)
        return f'ID: {self.ID}   Address: {self.get_address(time)}   {Rlist[len(Rlist)-1][0]} {Rlist[len(Rlist)-1][1]}  Delivery Deadline: {self.deliveryDeadLine}'
    
    def get_address(self, time):
        if self.ID == '9' and time < datetime.timedelta(hours=10, minutes=20):
            return "Unknown Address"
        
        else:
            return self.address