from threading import Thread
import serial
import serial.tools.list_ports


import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy
import math
import numpy.fft
import scipy.signal
import os
import time



liste_concentration =[]
temps=[]
t_acquisition= 20

fig=plt.figure()
line0, = plt.plot([],[])
Cmax = 5000

plt.title('Concentration CO2=f(temps)') # titre du graphique
plt.xlim(0, t_acquisition)
plt.ylim(0,Cmax)
plt.xlabel("temps en s")
plt.ylabel("Concentration CO2 en ppm")




# fonction à définir quand blit=True
# crée l'arrière de l'animation qui sera présent sur chaque image
def init():
    line0.set_data([],[])


    return line0,



def animate(i):

    line0.set_data(temps, liste_concentration)



ani = animation.FuncAnimation(fig,animate,frames = 10000,interval=20)

plt.show()


#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################


ne=2000
te=t_acquisition/ne





listeCO2 = numpy.zeros(ne,dtype=float)


liste_temps = numpy.zeros(ne,dtype=float)
ports = list(serial.tools.list_ports.comports())
for p in ports:

    print (p)
    if 'Arduino' in p.description :
        mData = serial.Serial(p.device,9600)


print(mData.is_open) #Print and check if the port is open
print(mData.name) # Print the name of the port
t_reel =0
for k in range(ne):

    while t_reel < t_acquisition:
        t_clock = time.time()
        line = mData.readline()  # Read the line from the serial port.
        print (line)
        temps.append(t_reel)
        listeDonnees = line.strip()
        listeDonnees = line.split() # on sépare l'abcisse et l'ordonnée

        print(listeDonnees)  # print the line in the console.
        if len(listeDonnees)!=0:
            concentration = float(listeDonnees[1].decode())
            listeCO2[k]= concentration
            liste_concentration.append(listeCO2[k])



        else :
            liste_concentration.append(liste_concentration[-1])

        t_clock_new = time.time()
        t_reel = t_reel + t_clock_new-t_clock # instant réel

        t_clock = t_clock_new
        print("t = %f"%(temps[k]))
        print("m = %f"%(liste_concentration[k]))
        # time.sleep((k+1)*te-t_reel) # calage sur le temps réel à chaque itération
        # time.sleep(2) # calage sur le temps réel à chaque itération


mData.close()






# plt.title('Concentration CO2=f(temps)') # titre du graphique
# plt.scatter(temps,liste_concentration, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
# plt.xlabel('temps en s')       # nommer l'axe des abscisses
# plt.ylabel('Concentration CO2 en ppm')       # nommer l'axe des ordonnéees
# # plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes
# # plt.ylim(min(liste_concentration),max(liste_concentration))
# plt.xlim (0,50)  #limtes pour les axes avec les valeurs extrêmes
# plt.ylim(0,10000)
#
# plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)


