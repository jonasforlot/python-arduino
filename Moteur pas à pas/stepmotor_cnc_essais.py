


#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  #############################################################################
import serial
import serial.tools.list_ports # pour la communication avec le port série
from nanpy import ArduinoApi    # importation des bibliothèques pour communication avec Arduino
from nanpy import SerialManager
from nanpy import Servo  # pour utiliser le servomoteur
from time import sleep    # pour faire des "pauses" dans l'exécution du programme
# import ctypes
# winmm = ctypes.WinDLL('winmm')
# winmm.timeBeginPeriod(1)
from GStiming import GS_timing




#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################
# Fonction pour la récupération du port COM venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description or  'CDC'in p.description or 'USB' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    return (mData.name) # Retourne le nom du port

port = recup_port_Arduino()
connection = SerialManager(device=port) #indiquer le bon port de la carte Arduino

a = ArduinoApi(connection=connection) #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)





#########################################   CODE ARDUINO  EN LANGAGE PYTHON    #################################################################################
stepPin = 3 #Y.STEP
dirPin = 6 # Y.DIR
enPin=8
stepsPerRev=200




a.pinMode(stepPin, a.OUTPUT)
a.pinMode(dirPin, a.OUTPUT)
a.pinMode(enPin, a.OUTPUT)
a.digitalWrite(enPin, a.LOW)
print("CNC Shield Initialized")

while True:
    print("Running clockwise")
    a.digitalWrite(6, a.HIGH) # Enables the motor to move in a particular direction
    #Makes 200 pulses for making one full cycle rotation

    for i in range (4*stepsPerRev):
        a.digitalWrite(stepPin, a.HIGH)
        GS_timing.delayMicroseconds(100)
        a.digitalWrite(stepPin, a.LOW)
        GS_timing.delayMicroseconds(1000)


    sleep(1)#One second delay
    print("Running counter_clockwise")
    a.digitalWrite(dirPin, a.LOW) #Changes the rotations direction


    # #Makes 400 pulses for making two full cycle rotation
    for i in range (2*stepsPerRev):
        a.digitalWrite(stepPin, a.HIGH)
        GS_timing.delayMicroseconds(100)
        a.digitalWrite(stepPin, a.LOW)
        GS_timing.delayMicroseconds(1000)

    sleep(1) #One second delay
