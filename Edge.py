class Edge:
    def __init__(self, address1, address2, length ):
        self.address1 = address1
        self.address2 = address2
        self.length = length
        self.ilength = int(float(length) * 10)


    def __str__(self):
        return f"Edge from {self.address1} to {self.address2}, Length: {self.length}"



        

