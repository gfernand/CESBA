def init():
    
    '''
    ->Models
    '0': Traditional
    '1': Sensors
    '2': Schedule
    '''

    global model
    model = 2

################ General #######################

    # Consume
    global consume_pc_on
    global consume_pc_standby
    global consume_light_byroom_medium
    global N_fluor_byroom_medium

    global offLights

    # All values as kWh
    N_fluor_byroom_medium = 7
    consume_light_byroom_medium = 36 * N_fluor_byroom_medium #W
    consume_pc_on = 75
    consume_pc_standby = consume_pc_on/25

    offLights = 23.00

    # Expenses / consume
    global price_watio

    price_watio = 0.15 #€/h

    # Time movement
    global time_by_step
    global speed

    time_by_step = 60 # seg/step
    speed = 0.7 # m/seg

############# TRADITIONAL #####################

    # Behaviour PC
    global time_to_set_standby_pc_from_on_whitout_usage
    time_to_set_standby_pc_from_on_whitout_usage = 0.10 #5min

################ SMART ########################

    # Sensors control
    global time_to_off_PC_from_standby
    global time_to_standby_PC_from_on
    global time_to_off_light

    time_to_off_PC_from_standby = 0.10
    time_to_standby_PC_from_on = 0.03
    time_to_off_light = 0.01

############# HVAC #####################

    #Climate
    global season
    season = 'summer'
    global setOffWorthIt


    global timeSetOnHVACBeforeGetT
    global timeSetOffHVACBeforeloseT

    global timeSetOnHVACBeforeGetTClass

    timeSetOnHVACBeforeGetT = 0.30
    timeSetOffHVACBeforeloseT = 0.30

    timeSetOnHVACBeforeGetTClass = 2.00

    setOffWorthIt = 2

    global temperatureSummerOut
    global temperatureSummerIn
    global temperatureSummerInMinimun
    global temperatureSummerInWithoutPeople
    global humiditySummerOut
    global humiditySummerIn
    global var #Tin = Tin0 +- var 
    global varTempertarueInInitialSummer
    global temperatureSummerInCorridors

    temperatureSummerIn = 24
    #                        0   1   2   3   4   5   6   7   8   9   10  11  12  13 14  15  16  17  18  19  20  21  22  23
    temperatureSummerOut = [25, 25, 24, 23, 22, 22, 22, 22, 23, 23, 25, 27, 30, 33, 35, 33, 36, 34, 33, 32, 29, 27, 26, 25] #Generical: [18, 18, 17, 17, 16, 16, 15, 16, 17, 20, 22, 24, 27, 28, 29, 30, 31, 31, 30, 29, 27, 25, 23, 19]
    temperatureSummerInMinimun = 22
    temperatureSummerInWithoutPeople = 25
    humiditySummerIn = 0.50
    humiditySummerOut = 0.65
    var = 1 # 1 degree Celsius
    varTempertarueInInitialSummer = 0
    temperatureSummerInCorridors = 26

    global temperatureWinterOut
    global temperatureWinterIn
    global temperatureWinterInMaximun
    global temperatureWinterInWithoutPeople
    global humidityWinterOut
    global humidityWinterIn
    global varTempertarueInInitialWinter

    temperatureWinterIn = 23
    temperatureWinterOut = [-2, -2, -2, -3, -3, -3, -4, -4, -3, -2, 0, 1, 3, 4, 5, 6, 5, 4, 3, 1, 0, -1, -2, -2]
    temperatureWinterInMaximun = 27
    temperatureWinterInWithoutPeople = 20
    humidityWinterIn = 0.45
    humidityWinterOut = 0.70
    varTempertarueInInitialWinter = 18

    #global timeToSetOffThermalZoneWithoutPeople
    global timeToReduceTemperatureThermalZoneWithoutPeople

    timeToReduceTemperatureThermalZoneWithoutPeople = 0.15 #30min
    #timeToSetOffThermalZoneWithoutPeople = 2.0 # 120 min
    
    #HVAC
    global powerHVAC
    global consume_hvac_on
    global consume_hvac_standby
    global TminSummer
    global TmaxSummer
    global TminWinter
    global TmaxWinter
    global timeGetTComfort
    global timeGetComfortValues

    powerHVAC =  0.8 #'50'% add on Power minimun in kWh
    consume_hvac_on = 1/3*0.8# % add on the powerHVAC 
    TminSummer = 22
    TmaxSummer = 30
    TminWinter = 20
    TmaxWinter = 25
    timeGetTComfort = 1 #minutes
    timeGetComfortValues = 1 #minutes

    global restRoomTemperature
    restRoomTemperature = 28
    #Thermal Zones
    #Thermal Zones control
    global timeToSampling #Sampling temperature time
    timeToSampling = 1 #Minutes

    #Thermal Zones values
    global UWall
    global URoof
    global UWindow
    global UInnerWall
    global CLTDWall
    global CLTDRoof
    global CLTDWindow
    global SCWindow
    global CLFWindow
    global MaxSHGFWindow
    global CFMByOccupant
    global airDensity
    global airSpecificHeat
    global waterSpecificHeat
    global ACH
    global peopleClass
    global peopleOffice
    global peopleLab
    global SHGByPerson
    global CLF
    global LHGByPerson
    global EffLights
    global EffEquipment

    UWall = 2 #W/m²xºc
    CLTDWall = {
    'N':[10, 10, 9, 8, 7, 5, 4, 3, 5, 6, 7, 8, 9, 10, 12, 13, 15, 17, 18, 19, 19, 19, 18, 16],
    'NE':[12, 11, 10, 8, 7, 5, 3, 5, 7, 14, 17, 20, 22, 23, 23, 24, 24, 25, 25, 24, 23, 22, 20, 18],
    'E':[13, 12, 9, 8, 7, 5, 5, 5, 7, 17, 22, 27, 30, 32, 33, 33, 32, 32, 31, 30, 28, 26, 24, 22],
    'SE':[14, 12, 9, 8, 6, 5, 4, 7, 7, 13, 17, 22, 26, 29, 31, 32, 32, 32, 31, 30, 28, 26, 24, 22],
    'S':[15, 13, 12, 9, 8, 8, 4, 5, 6, 6, 7, 9, 12, 16, 20, 24, 27, 29, 29, 29, 27, 26, 24, 22],
    'SW':[16, 14, 9, 8, 7, 5, 6, 6, 7, 8, 8, 8, 10, 12, 16, 21, 27, 32, 36, 38, 38, 37, 34, 31],
    'W':[21, 19, 12, 7, 6, 6, 8, 8, 9, 9, 9, 9, 10, 11, 14, 18, 24, 30, 36, 40, 41, 40, 38, 34],
    'NW':[18, 15, 13, 11, 9, 8, 8, 7, 8, 7, 7, 8, 9, 10, 12, 14, 18, 22, 27, 31, 32, 32, 30, 27]
    }
    URoof = 0.3 #W/m²xºC
    CLTDRoof = [22, 17, 13, 9, 6, 3, 1, 5, 11, 16, 22, 33, 38, 43, 51, 58, 62, 64, 55, 45, 38, 33, 26, 24]
    UWindow = 3.5 #W/m²xºc
    CLTDWindow = [1, 0, 0, 0, 0, 0, 0, 2, 4, 7, 9, 10, 12, 13, 14, 14, 13, 12, 10, 8, 6, 4, 3, 2]
    SCWindow = 0.8
    CLFWindow = {
    'N':[0.08, 0.07, 0.06, 0.06, 0.07, 0.73, 0.66, 0.65, 0.73, 0.80, 0.86, 0.89, 0.89, 0.86, 0.82, 0.75, 0.78, 0.91, 0.24, 0.18, 0.15, 0.13, 0.11, 0.10],
    'NE':[0.03, 0.02, 0.02, 0.02, 0.02, 0.56, 0.76, 0.74, 0.58, 0.37, 0.29, 0.27, 0.26, 0.24, 0.22, 0.20, 0.16, 0.13, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03],
    'E':[0.03, 0.02, 0.02, 0.02, 0.02, 0.47, 0.72, 0.80, 0.76, 0.62, 0.41, 0.27, 0.24, 0.22, 0.20, 0.17, 0.14, 0.11, 0.06, 0.05, 0.05, 0.04, 0.03, 0.03],
    'SE':[0.03, 0.03, 0.02, 0.02, 0.02, 0.30, 0.57, 0.74, 0.81, 0.79, 0.68, 0.49, 0.33, 0.28, 0.28, 0.22, 0.18, 0.13, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04],
    'S':[0.04, 0.04, 0.03, 0.03, 0.03, 0.09, 0.16, 0.23, 0.38, 0.58, 0.75, 0.83, 0.80, 0.68, 0.50, 0.35, 0.27, 0.19, 0.11, 0.09, 0.08, 0.07, 0.06, 0.05],
    'SW':[0.05, 0.05, 0.04, 0.04, 0.03, 0.07, 0.11, 0.14, 0.16, 0.19, 0.22, 0.38, 0.59, 0.75, 0.81, 0.81, 0.69, 0.45, 0.16, 0.12, 0.10, 0.09, 0.07, 0.06],
    'W':[0.05, 0.05, 0.04, 0.04, 0.03, 0.06, 0.09, 0.11, 0.13, 0.15, 0.16, 0.17, 0.31, 0.53, 0.72, 0.82, 0.81, 0.61, 0.16, 0.16, 0.12, 0.10, 0.07, 0.06],
    'NW':[0.05, 0.04, 0.04, 0.03, 0.03, 0.07, 0.11, 0.14, 0.17, 0.19, 0.20, 0.21, 0.22, 0.30, 0.52, 0.73, 0.82, 0.69, 0.16, 0.12, 0.10, 0.08, 0.07, 0.06]
    }
    MaxSHGFWindow = {'N':147, 'NE':565, 'E':671, 'SE':391, 'S':140, 'SW':391, 'W':671,'NW':565} #W/m²
    UInnerWall = 1.8 #W/m²xºC
    CFMByOccupant = 20
    airDensity = 1.19 #kg/m³
    airSpecificHeat = 1012 #J/(kg*K)
    waterSpecificHeat = 2257 #J/(kg*K)
    ACH = 4
    peopleClass = 30
    peopleOffice = 3
    peopleLab = 3
    SHGByPerson = 50 #W
    CLF = 1 #80%
    LHGByPerson = 40 #W
    EffLights = 0.6 #20%
    EffHVAC = 0.5 #50%
    EffEquipment = 0.8 #80%
