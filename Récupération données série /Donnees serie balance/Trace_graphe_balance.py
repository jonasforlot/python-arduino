#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_masse = [] # liste pour stocker les valeurs de masse

t_acquisition = 5.0
Massemax= 200


#pour le graphe en temps réel
def animate(i):
    line1 = mData.readline()
    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)


    if len(listeDonnees)!= 0 : # permet de nettoyer le flux de données acr seule une liste sur 3 contient des informations
        masse = float(listeDonnees[1].decode()) # après consulation des données, nous choisissons le 2ème élément de listeDonnees
        tempsmes = time.time()
        liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
        tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

        while tempsreel <= t_acquisition:
            liste_masse.append(masse)
            print("m = %f"%(masse), " g") # affichage de la valeur de la masse
            liste_temps.append(tempsreel)
            print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
            print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0
            line.set_data(liste_temps,liste_masse)
            return line,






# Fonction pour la récupération des données série venant du port USB
def recup_port_USB() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print (p)
        if 'USB' in p.description :
            Data = serial.Serial(p.device,9600)
    print(Data.is_open) #Print and check if the port is open
    print(Data.name) # Print the name of the port
    return Data






mData =recup_port_USB() #récupération des données

# Création figure
fig=plt.figure()
line, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(0,Massemax)
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

plt.show()
mData.close()
plt.close(fig)

#Ecriture dans un fichier txt
lines=['t\tm\n'] #première ligne du fichier txt
for i in range (len (liste_masse)):
    line = str(liste_temps[i]) +'\t'+ str(liste_masse[i])+'\n'
    lines.append(line)

fichier = open('data_balance.txt', 'w').writelines(lines) #création d'un nouveau fichier texte

