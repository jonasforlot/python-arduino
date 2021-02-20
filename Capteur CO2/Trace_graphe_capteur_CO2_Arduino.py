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
temps_reel =[]
t_acquisition= 20.0


class Update_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        #########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################


        te=1.0
        ne= int( t_acquisition/te)
        t0 =0.0
        t_mesure = 0




        listeCO2 = numpy.zeros(ne,dtype=float)


        liste_temps = numpy.zeros(ne,dtype=float)
        ports = list(serial.tools.list_ports.comports())
        for p in ports:

            print (p)
            if 'Arduino' in p.description :
                mData = serial.Serial(p.device,9600)


        print(mData.is_open) #Print and check if the port is open
        print(mData.name) # Print the name of the port




        for k in range(ne):
            #
            t_clock_old = time.time()
            print (time.time())
            line = mData.readline()  # Read the line from the serial port.
            print (line)


            listeDonnees = line.strip()
            listeDonnees = line.split() # on sépare l'abcisse et l'ordonnée

            print(listeDonnees)  # print the line in the console.
            if len(listeDonnees)!=0:
                concentration = float(listeDonnees[1].decode())
                listeCO2[k]= concentration
                liste_concentration.append(listeCO2[k])
                print("C_CO2 = %f"%(liste_concentration[k]))
                print (time.time())
                t_clock_new = time.time()
                t_mesure = t_mesure + t_clock_new-t_clock_old # instant réel
                temps.append(t_mesure)
                temps_reel.append(t_mesure -temps[0])
                print("t = %f"%(temps_reel[k]))
                t_clock_old = t_clock_new



            else :
                pass





        mData.close()


class Graph_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):


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

            line0.set_data(temps_reel, liste_concentration)



        ani = animation.FuncAnimation(fig,animate,frames = 1000,interval=20)

        plt.show()



class Main_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        UpdateThread = Update_thread()         # Create the thread Update.
        UpdateThread.start()                   # Start the thread Update.

        graphThread =Graph_thread()
        graphThread.start()




if __name__ == "__main__":

    import sys
    MainThread = Main_thread()
    MainThread.start()

