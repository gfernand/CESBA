import random

def init():
 
	global time_by_step
	global speed
	global activationFire
	global Out1
	global OutBuildingC

	time_by_step = 60 # seg/step
	speed = 0.7 # m/seg
	#meter aqui las velocidad de los ancianos
	Out1 = (14,2)
	OutBuildingC = (98,16)
	#hora = random.randint(8,20)
	#minute = random.randint(00,59)
	horasFuego = [9.15,10.00 , 11.30, 13.05, 15.30, 17.45, 19.15, 20.00]
	activationFire = 9.15#random.choice(horasFuego)
	print("La hora del fuego es: ", activationFire,".")