

#-------------------------------------------------------------------------------
# Name:        Elab_Force_niv0
# Purpose:     Programme d'utilisation du capteur Eurosmart de pression résistive (force) Elab_Force.
#              Le capteur utilise 2 broches analogiques de la carte EDUCA DUINO Lab pour les mesures de tension et de courant.
#              Les mesures sont affichées sur l'écran LCD 2 lignes, 16 colonnes.
# Author:      cletourneur
#
# Created:     30/01/2019
# Copyright:   (c) cletourneur 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  #############################################################################


from nanpy import SerialManager     # Utiliser par l'interpreteur python pour communiquer
                                    # avec la carte EDUCA DUINO LAB
from nanpy import ArduinoApi        # Utilisation des services arduino.
from threading import Thread
from eurosmart import *             # Utilisation de la librairie Eurosmart pour piloter le capteur Elab_Force
from nanpy import Lcd               # Utilisation de l'écran LCD 2*16
import sys
import serial.tools.list_ports
from time  import sleep
import sys
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Listes utilisées pour recueillir les mesures.
liste_temps=[]
liste_concentration =[]

class Graph_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):


        fig=plt.figure()
        line0, = plt.plot([],[])
        Cmax = 5000
        tmax = 20
        plt.title('Concentration CO2=f(temps)') # titre du graphique
        plt.xlim(0, tmax)
        plt.ylim(0,Cmax)
        plt.xlabel("temps en s")
        plt.ylabel("Concentration CO2 en ppm")




        # fonction à définir quand blit=True
        # crée l'arrière de l'animation qui sera présent sur chaque image
        def init():
            line0.set_data([],[])


            return line0,



        def animate(i):

            line0.set_data(liste_temps, liste_concentration)



        ani = animation.FuncAnimation(fig,animate,frames = 500,interval=500)

        plt.show()

class Update_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # # ###############  COMMUNICATION AVEC CARTE ARDUINO############################


        def detectePortArduino():
            """
            Détecte le port série USB où est connectée la carte Arduino
            .
            """

            portCom = serial.tools.list_ports.comports()
            ports = list(serial.tools.list_ports.comports())
            print (ports)
            for p in ports:
                # print (p.device)
                # print (p.vid)
                # print (p.pid)


                if ((p.vid==9025) and (p.pid==66) ):
                    print('Carte EDUCADUINO connectée')
                    print ('port : ', p.device)
                    print ('vid : ', p.vid)
                    print ('pid : ', p.pid)
                    return (p.device)


                pass

                if ((p.vid==9025 or p.vid==10755) and (p.pid==67 or p.pid==1)):
                    print('Carte ARDUINO connectée')
                    print ('port : ', p.device)
                    print ('vid : ', p.vid)
                    print ('pid : ', p.pid)
                    return (p.device)

                pass





        #########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################

        #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)

        portCom = detectePortArduino()
        if (portCom == None  ):
            print('Pas de carte  connectée au PC')
            sys.exit();                                     # Sortie du programme.

        connection = SerialManager(device=portCom)          # Numéro de port utilisé par la carte.

        # connection = SerialManager(device='COM29') #indiquer le bon port de la carte Arduino
        try:
            a = ArduinoApi(connection=connection)
            print("La librairie nanpy est téléversée dans la carte ")


        except:
            print("La librairie nanpy n'a pas été téléversée dans la carte ")

        a.pinMode(11,a.OUTPUT) # Broches déclarée comme sorties pour allumer les LED
        a.pinMode(3,a.OUTPUT)
        a.pinMode(2,a.OUTPUT)


        # Initialisation de l'écran LCD de 2 lignes de 16 caractères
        # connecté à la cartes avec les broches 12, 11, 5, 4, 3, 2
        lcd = Lcd([8,9,4,5,6,7], [16,2], connection=connection)
        lcd.clear()                                 # Efface l'écran et positionne le curseur en 1ère colonne, 1ère ligne.
        lcd.printString("Hello !")
        time.sleep(1)



        t_reel=0
        t_reel_fin=20
        t_clock = time.time()
        while t_reel<t_reel_fin:

            SensorValue=a.analogRead(1)
            total = 0
            totalA2 = 0




            for i in range (50):
                total += a.analogRead(1)
                totalA2 += a.analogRead(1)
            voltage = (total/50)*5000/1023

            if voltage == 0:
                print("Problème")
                lcd.clear()
                lcd.printString("Problème")
            elif voltage<400 :
                print("Préchauffage")
                lcd.clear()
                lcd.printString("Préchauffage")
            else:
                voltage_difference = voltage-400
                concentration = float(round(voltage_difference *50/16,2))
                liste_concentration.append(concentration)
                print("CO2 : ",concentration," ppm")
                lcd.clear()
                lcd.printString("CO2 : ",0,0)
                lcd.printString(concentration)
                lcd.printString(" ppm")

            if  concentration < 800 :    #allumage des LED
                a.digitalWrite (2,a.HIGH)
                a.digitalWrite (3,a.LOW)
                a.digitalWrite (11,a.LOW)
            elif  concentration > 1600 :
                a.digitalWrite (2,a.LOW)
                a.digitalWrite (3,a.LOW)
                a.digitalWrite (11,a.HIGH)
            else :
                a.digitalWrite (2,a.LOW)
                a.digitalWrite (3,a.HIGH)
                a.digitalWrite (11,a.LOW)
            lcd.printString("A2 :",0,1)
            lcd.printString(totalA2/50)
            print(";A2 : ",totalA2/50,)

            t_clock_new = time.time()
            t_reel = t_reel + t_clock_new-t_clock # instant réel
            liste_temps.append(float(t_reel))
            t_clock = t_clock_new

            Cmin = 0
            Cmax = 10000
            tmax = 50


# plt.title('Concentration CO2=f(temps)') # titre du graphique
# plt.scatter(liste_temps,liste_concentration, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
# plt.xlabel('temps en s')       # nommer l'axe des abscisses
# plt.ylabel('Concentration CO2 en ppm')       # nommer l'axe des ordonnéees
# # plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes
# # plt.ylim(min(liste_concentration),max(liste_concentration))
# plt.xlim (0,50)  #limtes pour les axes avec les valeurs extrêmes
# plt.ylim(0,10000)
#
# plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)



class Main_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        UpdateThread = Update_thread()         # Create the thread Update.
        graphThread =Graph_thread()
        UpdateThread.start()                   # Start the thread Update.

        graphThread.start()
        # graphThread.join()
        # UpdateThread.join()                   # Start the thread Update.




if __name__ == "__main__":

    import sys
    MainThread = Main_thread()
    MainThread.start()
    # MainThread.join()



