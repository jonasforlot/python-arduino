# -*- coding: utf-8 -*-
"""
Radar de recul avec LED d'alerte:
On veut mesurer une distance à partir de la mesure du temps de parcours d’une onde ultrasonore qui se réfléchit sur un obstacle. On utiliser pour cela un module ultrason HC-SR04
On fera clignoter des LED de couleurs différentes (rouge, orange, verte) selon la position de l’obstacle par rapport au capteur US, de plus en pus vite selon la zone.
Un buzzer émet des bips de plus en plus rapides et plus aigus qaund on s'approche de l'obstacle
Zone verte : entre 30 cm et 50 cm
Zone orange : entre 10 cm et 30 cm
Zone rouge : moins de 10 cm

"""
#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  #############################################################################

from nanpy import ArduinoApi  # importation des bibliothèques pour communication avec Arduino
from nanpy import SerialManager
from nanpy import Ultrasonic # pour utiliser le module HC-SR04
from time import sleep  # pour faire des "pauses" dans l'exécution du programme


#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################

connection = SerialManager(device='COM7') #indiquer le bon port de la carte Arduino

a = ArduinoApi(connection=connection)  #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)

capteurUltraSon = Ultrasonic(echo=12, trig=13, useInches=False, connection=connection) # Branchements du capteur

LED_verte = 8 #broches pour les LED (montage en série avec une résistance de 220 ohms)
LED_orange = 9
LED_rouge = 10
buzzer = 11 # broche pour le buzzer
a.pinMode(LED_verte,a.OUTPUT) #ces broches sont déclarées comme sorties
a.pinMode(LED_orange,a.OUTPUT)
a.pinMode(LED_rouge,a.OUTPUT)
a.pinMode (buzzer,a.OUTPUT)

#########################################   CODE ARDUINO  EN LANGAGE PYTHON    #################################################################################

while True :

    # Mesure de la durée pris par le son pour faire l'Aller/Retour entre le capteur US et l'obstacle.
    duree_µs = capteurUltraSon.get_duration()
    duree_s  = duree_µs/1000000.0             # Conversion µs en s
    print ('durée aller retour = ',duree_s)

    VITESSE_SON = 340.0                    #vitesse du son dans l'air en m/s
    distanceAllerRetour_s = VITESSE_SON * duree_s;
    distance_m = distanceAllerRetour_s / 2	#Distance jusqu'a l'obstacle.
    print ('distance en m = ', distance_m)


    if distance_m <  0.5 and distance_m > 0.3 : #zone pour laquelle la LED verte clignote , buzzer à 440 Hz

        a.digitalWrite (LED_verte, a.HIGH)  #la LED s'allume pendant 1 s et s'éteint pendant 0,5 s
        a.tone(buzzer,440)                    #buzzer à 440 Hz
        sleep(1)
        a.digitalWrite (LED_verte,a.LOW)
        a.noTone(buzzer)
        sleep (0.5)





    if distance_m < 0.3 and distance_m > 0.1: #zone pour laquelle la LED orange clignote , buzzer à 880 Hz

        a.digitalWrite (LED_orange, a.HIGH) #la LED s'allume pendant 0,5 s et s'éteint pendant 0,25 s
        a.tone(buzzer,880)                #buzzer à 880 Hz
        sleep(0.5)
        a.digitalWrite (LED_orange,a.LOW)
        a.noTone(buzzer)
        sleep (0.25)



    if distance_m < 0.1:  #zone pour laquelle la LED rouge clignote , buzzer à 1760 Hz

        a.digitalWrite (LED_rouge,a.HIGH) #la LED s'allume pendant 0,1 s et s'éteint pendant 0,05 s
        a.tone(buzzer,1760)            #buzzer à 1760 Hz
        sleep (0.1)
        a.digitalWrite (LED_rouge,a.LOW)
        a.noTone(buzzer)
        sleep (0.05)





    sleep(0.5)
