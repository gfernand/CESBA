from mesa import Agent, Model
import configuration.settings

class Time(Agent):

    def __init__(self):

        self.timeByStep = configuration.settings.time_by_step
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.seg = 0
        self.clock = 00.00

    def step(self):
        self.seg = self.seg + self.timeByStep
        if self.seg > 59:
            self.seg = self.seg - 60
            self.minute = self.minute + 1
            if self.minute > 59:
                self.minute = self.minute - 60
                self.hour = self.hour + 1
                if self.hour > 23:
                    self.hour = self.hour - 24
                    self.day = self.day + 1
        self.clock = (self.hour*100 + self.minute) / 100
        print('Day: ', (self.day + 1), ' - Hour: ', self.clock)

    def getCorrectHour(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        response = hour
        if dec > 0.59:
            responseH = int(hour) + 1
            responseD = dec - 0.60
            response = responseH + responseD
        return round(response,2)

    def getDownCorrectHour(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        response = hour
        if dec > 0.59:
            responseH = int(hour)
            responseD = dec - 0.40
            response = responseH + responseD
        return round(response,2)

    def getMinuteFromHours(self, hour):
        dec = float('0'+str(hour-int(hour))[1:])
        uni = float(int(hour))
        minutes = dec*100 + uni*60
        return minutes