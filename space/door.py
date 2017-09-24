class Door():

    def __init__(self, x, y):
        self.state = False
        self.x = x
        self.y = y
        
    def open(self):
        self.state = True
       

    def close(self):
        self.state = False
