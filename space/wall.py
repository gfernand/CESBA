class Wall():

    def __init__(self, l1, l2, room1 = False, room2 = False, orientation = False):
        self.orientation = orientation
        self.l1 = l1
        self.l2 = l2
        self.room1 = room1
        self.room2 = room2