class Room():

    def __init__(self, name, typeRoom, conectedTo, nameThermalZone, dx, dy, dh, jsonWindows, pos = (0,0)):
        self.name = name
        self.typeRoom = typeRoom
        self.conectedTo = conectedTo
        self.dx = dx
        self.dy = dy
        self.dh = dh
        self.pos = pos
        self.jsonWindows = jsonWindows
        self.roomsConected = []
        self.roomsAdj = []
        self.light = False
        self.PCs = []
        self.agentsInRoom = []
        self.walls = []
        self.innerWalls = []
        self.doors = []
        self.windows = []
        self.nameThermalZone = nameThermalZone
        self.thermalZone = False
        self.waitedUsers = 0
        self.entrance = None