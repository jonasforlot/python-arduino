#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_distance = [] # liste pour stocker les valeurs de distance

t_acquisition = 6.0
distancemax= 500 # en mm


#pour le graphe en temps réel
def animate(i):
    line1 = Data.readline()
    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)


    if len(listeDonnees)!= 0 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        distance = float(listeDonnees[4].decode()) # après consulation des données, nous choisissons le 5ème élément de listeDonnees
        tempsmes = time.time()
        liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
        tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

        while tempsreel <= t_acquisition:
            liste_distance.append(distance)
            print("d = %f"%(distance), " mm") # affichage de la valeur de la distance
            liste_temps.append(tempsreel)
            print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
            print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0
            line.set_data(liste_temps,liste_distance)
            return line,






# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
        # if 'CDC' in p.description :    #pour les utilisateurs de mac
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port 
    return mData






Data =recup_port_Arduino() #récupération des données

# Création figure
fig=plt.figure()
line, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(0,distancemax)
plt.xlabel('temps en s')
plt.ylabel('distance en mm')
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

plt.show()

plt.close(fig)
Data.close()
#Ecriture dans un fichier txt
lines=['t\td\n'] #première ligne du fichier txt
for i in range (len (liste_distance)):
    line = str(liste_temps[i]) +'\t'+ str(liste_distance[i])+'\n'
    lines.append(line)

fichier = open('data_arduino.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte

