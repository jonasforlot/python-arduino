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

t_acquisition = 50.0
Massemax= 200

#Ecriture dans un fichier txt
lines=['t\tm\n'] #première ligne du fichier txt

#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1
    line1 = Data.readline()
    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)


    if len(listeDonnees)!= 0 : # permet de nettoyer le flux de données car seule une liste sur 3 contient des informations
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
            line0.set_data(liste_temps,liste_masse)
            line = str(liste_temps[-1]) +'\t'+ str(liste_masse[-1])+'\n'
            lines.append(line)
            fichier = open('U:\Documents\essais Python\Améliorations\Données série balance\data_balance.txt', 'w')
            fichier.writelines(lines) #création d'un nouveau fichier texte
            return line0,






# Fonction pour la récupération des données série venant du port USB
def recup_port_USB() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print (p)
        if 'USB' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData






Data =recup_port_USB() #récupération des données

# Création figure
fig=plt.figure()
line0, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(0,Massemax)
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=20000,  interval=20,repeat=False)

plt.show()
Data.close()
plt.close(fig)




