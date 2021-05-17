#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
# import time # gestion du temps
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit


liste_a = [] # liste pour stocker les valeurs de distance
liste_t = []
liste_tension = []
t_acquisition = 10.0 # en s
amax =2 # en g
amin= -2 # en g
Umax= 5.0

# dt=0.1
# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description or  'CDC'in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData


Data =recup_port_Arduino() #récupération des données    

temps =0
while temps <= t_acquisition:
    line = Data.readline()


    print (line)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line.split()
    print (listeDonnees)




    if len(listeDonnees) == 15 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        accel = (float(listeDonnees[5].decode()))/16834 # après consulation des données, nous choisissons le 6 ème élément de listeDonnees, on convertit l'accélération en g


        temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 1er élément de listeDonnees
        
        tension = float(listeDonnees[14].decode()) # après consulation des données, nous choisissons le 14ème élément de listeDonnees



        
        liste_a.append(accel)
        print("a = %f"%(accel), " g") # affichage de la valeur de l'accélération
        liste_tension.append(tension)
        print("tension = %f"%(tension), " V") # affichage de la valeur de l'accélération
        liste_t.append(temps)
        




Data.close()





fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
ax1.set_title('accélération=f(t)') # titre du graphique
ax1.scatter(liste_t,liste_a, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('accélération en g')
ax1.axis([min(liste_t),max(liste_t),min(liste_a),max(liste_a)])  

ax2.set_title('tension=f(t)') # titre du graphique
ax2.scatter(liste_t,liste_tension, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax2.set_xlabel('temps en s')
ax2.set_ylabel('tension en V')
ax2.axis([min(liste_t),max(liste_t),min(liste_tension),max(liste_tension)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)

#Ecriture dans un fichier txt
lines=['t\ta\tU\n'] #première ligne du fichier txt
for i in range (len (liste_t)):
    line = str(liste_t[i]) +'\t'+ str(liste_a[i])+'\t'+ str(liste_tension[i])+'\n'
    lines.append(line)

fichier = open('data_accelerometre.txt', 'w').writelines(lines) #création d'un nouveau fichier texte
