class Package:
    def __init__(self, ID , address, city, state, zip, deliveryDeadLine, weight, notes):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadLine = deliveryDeadLine
        self.weight = weight
        self.status = "at hub"
        self.deliveryTime = None
        self.notes = notes

    

    def __str__(self):
        return f"Package ID: {self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, Zip: {self.zip}, Delivery Deadline: {self.deliveryDeadLine}, Weight: {self.weight}, Status: {self.status}"