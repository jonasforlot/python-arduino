#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_T = [] # liste pour stocker les valeurs de température
liste_P = [] # liste pour stocker les valeurs de température

t_acquisition = 1000.0
Tmax= 110.0 # en °C
Pmax =140000.0 # en Pa


#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1,t0,t1,u0,u1
    line_data = Data.readline()
    print (line_data)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line_data.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line_data.split()
    print (listeDonnees)


    if len(listeDonnees)== 11 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 3ème élément de listeDonnees
        temp = float(listeDonnees[5].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        pression = float(listeDonnees[9].decode()) # après consulation des données, nous choisissons le 10ème élément de listeDonnees

        while temps <= t_acquisition:
            liste_T.append(temp)
            print("Température = %f"%(temp)) # affichage de la valeur de la distance
            liste_temps.append(temps)
            print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
            liste_P.append(pression)
            print("Pression = %f"%(pression)) # affichage de la valeur de la distance
            line0.set_data(liste_temps,liste_T)
            line1.set_data(liste_temps,liste_P)

            return line0,line1,







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
fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
line0, = ax1.plot([],[])
line1, = ax2.plot([],[])
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([0,t_acquisition,0,Tmax])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([0,t_acquisition,0.0,Pmax])




#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)

plt.show()

# plt.close(fig)
Data.close() # pour arrêter la lecture des données série


fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
line0, = ax1.plot([],[])
line1, = ax2.plot([],[])
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([0,t_acquisition,0,Tmax])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([0,t_acquisition,0.0,Pmax])

ax1.set_title('température=f(t)') # titre du graphique
ax1.scatter(liste_temps,liste_T, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([min(liste_temps),max(liste_temps),min(liste_T),max(liste_T)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température

ax2.set_title('pression=f(t)') # titre du graphique
ax2.scatter(liste_temps,liste_P, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([min(liste_temps),max(liste_temps),min(liste_P),max(liste_P)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)

#Ecriture dans un fichier txt
lines=['t\tT\tP\n'] #première ligne du fichier txt
for i in range (len (liste_T)):
    line = str(liste_temps[i]) +'\t'+ str(liste_T[i])+'\t'+ str(liste_P[i])+'\n'
    lines.append(line)

fichier = open('P:\Mes documents\essais Python\Améliorations\Données série PvapSat\data_arduinobis.txt', 'w').writelines(lines) #création d'un nouveau fichier texte

