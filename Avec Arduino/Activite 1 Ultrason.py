# -*- coding: utf-8 -*-
"""
Radar de recul :
On veut mesurer une distance à partir de la mesure du temps de parcours d’une onde ultrasonore qui se réfléchit sur un obstacle. On utiliser pour cela un module ultrason HC-SR04
"""

#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  #############################################################################


from nanpy import ArduinoApi    # importation des bibliothèques pour communication avec Arduino
from nanpy import SerialManager
from nanpy import Ultrasonic  # pour utiliser le module HC-SR04
from time import sleep   # pour faire des "pauses" dans l'exécution du programme


#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################


connection = SerialManager(device='COM9') #indiquer le bon port de la carte Arduino

a = ArduinoApi(connection=connection)  #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)

capteurUltraSon = Ultrasonic(echo=12, trig=13, useInches=False, connection=connection) # Branchements du capteur

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
    sleep(0.5)
