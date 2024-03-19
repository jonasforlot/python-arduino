
#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps


#initialisation des listes


liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_rps = [] # liste pour stocker les valeurs de température
liste_P = [] # liste pour stocker les valeurs de pression


t_acquisition = 1000.0
Tmax= 5 # en rps
Pmax =140000.0 # en Pa


#Ecriture dans un fichier txt
lines=['t\trps\tP\n'] #première ligne du fichier txt
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




    if len(listeDonnees)== 3 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = (float(listeDonnees[0].decode()))/1000.0 # après consulation des données, nous choisissons le 3ème élément de listeDonnees
        rps = float(listeDonnees[1].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        pression = float(listeDonnees[2].decode()) # après consulation des données, nous choisissons le 10ème élément de listeDonnees


        while temps <= t_acquisition:
            liste_rps.append(rps)
            print("Vitesse = %f"%(rps)) # affichage de la valeur de la température
            liste_temps.append(temps)
            print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
            liste_P.append(pression)
            print("Pression = %f"%(pression)) # affichage de la valeur de la pression
            line0.set_data(liste_temps,liste_rps)
            line1.set_data(liste_temps,liste_P)


            line = str(liste_temps[-1]) +'\t'+ str(liste_rps[-1])+'\t'+ str(liste_P[-1])+'\n'
            lines.append(line)
            fichier = open('U:\Documents\data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte,indiquer le bon chemin
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
ax1.set_ylabel('vitesse en rps')
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
ax1.set_title('rps=f(t)') # titre du graphique
ax1.scatter(liste_temps,liste_rps, color ='r', marker = 'o') # On affiche les points de coordonnées (t,T) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('vitesse en rps')
ax1.axis([min(liste_temps),max(liste_temps),min(liste_rps),max(liste_rps)])  #limites pour les axes avec les valeurs extrêmes de temps et de température


ax2.set_title('pression=f(t)') # titre du graphique
ax2.scatter(liste_temps,liste_P, color ='b', marker = 'o') # On affiche les points de coordonnées (t,P) avec des points bleus
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([min(liste_temps),max(liste_temps),min(liste_P),max(liste_P)])  #limites pour les axes avec les valeurs extrêmes de temps et de pression
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)








