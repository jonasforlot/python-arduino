#importation des modules
import serial
import serial.tools.list_ports   # pour la communication avec le port série
import matplotlib.pyplot as plt # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps
from threading import Thread  # pour faire de la programmation parallèle

#initialisation des listes
liste_temps = []
liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_distance = [] # liste pour stocker les valeurs de distance

t_acquisition = 5.0
distancemax= 500 # en mm

# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
        # if 'CDC' in p.description :    #pour les utilisateurs de mac
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) #Print and check if the port is open
    print(mData.name) # Print the name of the port
    return mData
def ecriture_txt(t,d):
    #Ecriture dans un fichier txt
    lines=['t\td\n'] #première ligne du fichier txt
    for i in range (len (t)):
        line = str(t[i]) +'\t'+ str(d[i])+'\n'
        lines.append(line)

    fichier = open('data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte



# Création d'une classe pour créer un fil d'exécution (sous programme) permettant de tracer le graphe au fur et à mesure à partir des données stockées dans les listes
class dynamic_Graph_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        #pour le graphe en temps réel
        def animate(i):
            line.set_data(liste_temps,liste_distance)
            return line,

        # Création figure
        fig=plt.figure()
        line, = plt.plot([],[])
        plt.xlim(0, t_acquisition)
        plt.ylim(0,distancemax)
        plt.grid()

        ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

        plt.show()






# Création d'une classe pour créer un fil d'exécution (sous programme) permettant de récupérer les données série et les stocker dans les listes
class Update_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        mData =recup_port_Arduino()
        tempsreel=0
        while tempsreel <= t_acquisition:
            line1 = mData.readline()
            print (line1)
            #on retire les caractères d'espacement en début et fin de chaîne
            listeDonnees = line1.strip()
            # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
            listeDonnees = line1.split()
            print (listeDonnees)

            if len(listeDonnees)!= 0: # permet de nettoyer le flux de données acr seule une liste sur 3 contient des informations
                distance = float(listeDonnees[4].decode()) # après consulation des données, nous choisissons le 5ème élément de listeDonnees
                tempsmes = time.time()
                liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
                tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

                liste_distance.append(distance)
                print("d = %f"%(distance), " mm") # affichage de la valeur de la masse
                liste_temps.append(tempsreel)
                print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
                print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0

        mData.close()
        ecriture_txt(liste_temps,liste_distance)

# Fil d'exécution principale
class Main_thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        UpdateThread = Update_thread()         # Create the thread Update.
        UpdateThread.start()                   # Start the thread Update.

        dynamicGraphthread =dynamic_Graph_thread()
        dynamicGraphthread.start()







if __name__ == "__main__":

    import sys
    MainThread = Main_thread()
    MainThread.start()
    MainThread.join() # pas vraiment compris à quoi sert le join ... mais c'est conseillé on dirait !







