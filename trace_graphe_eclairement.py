
#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
# import time # gestion du temps
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit
import os


liste_e = [] # liste pour stocker les valeurs d'éclairement
liste_t = []
t_acquisition = 10.0 # en s
emax =7000 # en lux
emin= 0 # en lux


# dt=0.1




#pour le graphe en temps réel
def animate(i):
    line1 = Data.readline()


    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)




    if len(listeDonnees) == 6 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        eclairement = (float(listeDonnees[4].decode()))/16834 # après consulation des données, nous choisissons le 4 ème élément de listeDonnees, on convertit l'accélération en g


        temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 2ème élément de listeDonnees


        while temps <= t_acquisition:
            liste_e.append(eclairement)
            print("Eclairement = %f"%(eclairement), " lux") # affichage de la valeur de l'eclairement
            liste_t.append(temps)
            print("temps = %f"%(temps), " s") # affichage de la valeur du temps en partant de 0
            line.set_data(liste_t,liste_e)
            return line,












# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData












Data =recup_port_Arduino() #récupération des données


# Création figure
fig=plt.figure()
line, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(emin,emax)
plt.xlabel('temps en s')
plt.ylabel('éclairement en lux')
plt.grid()




#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)


plt.show()


plt.close(fig)
Data.close()







# Nom de base pour les fichiers
nom_fichier_base = "eclairement"
compteur = 0

# Chercher un nom de fichier disponible (eclairement0.txt, eclairement1.txt, etc.)
while os.path.exists(f"{nom_fichier_base}{compteur}.txt"):
    compteur += 1

nom_fichier = f"{nom_fichier_base}{compteur}.txt"

# Ecriture dans un fichier txt
lines = ['t\ta\n']  # première ligne du fichier txt
for i in range(len(liste_e)):
    line = str(liste_t[i]) + '\t' + str(liste_e[i]) + '\n'
    lines.append(line)

# Création du fichier texte avec le compteur
with open(nom_fichier, 'w') as fichier:
    fichier.writelines(lines)

print(f"Fichier créé : {nom_fichier}")






t = np.array(liste_t)
ecl = np.array(liste_e)





texte = 'Eclairement en fonction du temps'

# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure()
plt.scatter(t, ecl, c = 'red', marker = '+')
plt.plot(t,ecl,label = texte)
plt.xlabel("Temps en s")
plt.ylabel("Eclairement en lux")
plt.legend()   # pour afficher les légendes (label)
plt.show()




