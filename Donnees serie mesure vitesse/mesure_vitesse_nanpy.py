from nanpy import SerialManager     # Utiliser par l'interpreteur python pour communiquer
                                    # avec la carte EDUCA DUINO LAB
from nanpy import ArduinoApi        # Utilisation des services arduino.


import time
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée

#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################


connection = SerialManager(device='COM21') #indiquer le bon port de la carte Arduino

a = ArduinoApi(connection=connection)  #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)

#initialisation des listes
liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_rps = [] # liste pour stocker les valeurs de vitesse

t_acquisition = 10.0
rpsmax= 250 # en mm
nb_trous = 20 # nombre de trous de la roue codeuse

def comptage(T_comptage) :
    compt = 0;
    start_time=time.time() # on mesure le temps
    end_time=start_time+T_comptage # pour un comptage tous les T_comptage
    temps = time.time() # mesure du temps pour l'acquisition
    etat_new = False
    etat_old = False

    while(time.time()<end_time) :
        # comptage sur T_comptage
        if (a.analogRead(0)< 30):
            etat_new = True

        else :
            etat_new =False

        if (etat_old != etat_new) :
            etat_old = etat_new
            compt = compt + 1
    return compt








def main():


    #pour le graphe en temps réel
    def animate(i):


            tempsmes = time.time()
            liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
            tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)
            compt= comptage (1)
            print (compt)




            while tempsreel <= t_acquisition:

                rps = float(compt)/(2*nb_trous)
                liste_rps.append(rps)
                print("rps = %f"%(rps)) # affichage de la valeur de la distance
                liste_temps.append(tempsreel)
                print("temps mesuré = %f"%(tempsreel), " s") # affichage de la valeur du temps absolu
                line.set_data(liste_temps,liste_rps)
                return line,




    # Création figure
    fig=plt.figure()
    line, = plt.plot([],[])
    plt.xlim(0, t_acquisition)
    plt.ylim(0,rpsmax)
    plt.xlabel('temps en s')
    plt.ylabel('rps')
    plt.grid()


    #Animation
    ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

    plt.show()

    plt.close(fig)



    plt.title('rps=f(t)') # titre du graphique
    plt.scatter(liste_temps,liste_rps, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
    plt.xlabel('temps en s')
    plt.ylabel('rps')
    plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de I et de U
    plt.ylim(min(liste_rps),max(liste_rps))
    plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)

    #Ecriture dans un fichier txt
    lines=['t\trps\n'] #première ligne du fichier txt
    for i in range (len (liste_rps)):
        line = str(liste_temps[i]) +'\t'+ str(liste_rps[i])+'\n'
        lines.append(line)

    fichier = open('p:\Mes documents\essais Python\Mesure vitesse\data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte










    pass

if __name__ == '__main__':
    main()
