# -*- coding: utf-8 -*-
"""
Programme Python pour montage Arduino ouverture automatique de porte de poulailler
Partie capteur :
la photorésistance est privée de lumière (quand la nuit tombe) ou est éclairée.

Partie actionneur  :
Selon l’éclairement reçu par la photorésistance, le servomoteur prend une position à 45° ou 90°.
"""
#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  #############################################################################

from nanpy import ArduinoApi    # importation des bibliothèques pour communication avec Arduino
from nanpy import SerialManager
from nanpy import Servo  # pour utiliser le servomoteur
from time import sleep    # pour faire des "pauses" dans l'exécution du programme

#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################
connection = SerialManager(device='COM17') #indiquer le bon port de la carte Arduino

a = ArduinoApi(connection=connection) #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)

servo = Servo(9, connection=connection) # on attribue la broche 9 pour l'instruction donné au servomoteur



#########################################   CODE ARDUINO  EN LANGAGE PYTHON    #################################################################################


while True:
    Valeur_A0=a.analogRead(0) # lecture de la tension sur l'entrée analogique A0 (valeur comprise entre 0 et 1023 qui correspond à une tension entre 0 et 5V)
    Tension_A0=Valeur_A0*5.0/1023 # conversion de la valeur en V
    if (Tension_A0<4.0):    # Selon la tension lue, la position du servomoteur est de 90° ou 45° (ici on a choisi comme valeur de référence : 4V)
        servo.write(90)


    else:
        servo.write(45)

    print (Tension_A0)
    sleep(0.25)
