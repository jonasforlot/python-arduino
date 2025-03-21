#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps


#initialisation des listes


liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_T = [] # liste pour stocker les valeurs de température
liste_T2 = [] # liste pour stocker les valeurs de température


liste_P = [] # liste pour stocker les valeurs de pression


t_acquisition = 1000.0
Tmax= 110.0 # en °C
Pmax =140000.0 # en Pa


#Ecriture dans un fichier txt
lines=['t\tT1\tT2\tP\n'] #première ligne du fichier txt
#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1,line2,t0,t1,u0,u1
    line_data = Data.readline()
    print (line_data)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line_data.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line_data.split()
    print (listeDonnees)




    if len(listeDonnees)== 15 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 3ème élément de listeDonnees
        temp = float(listeDonnees[5].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        temp2 = float(listeDonnees[9].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        pression = float(listeDonnees[13].decode()) # après consulation des données, nous choisissons le 10ème élément de listeDonnees


        while temps <= t_acquisition:
            liste_temps.append(temps)
            print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps
            liste_T.append(temp)
            print("Température 1 = %f"%(temp)) # affichage de la valeur de la température
            liste_T2.append(temp2)
            print("Température 2 = %f"%(temp2)) # affichage de la valeur de la température
            liste_P.append(pression)
            print("Pression = %f"%(pression)) # affichage de la valeur de la pression
            line0.set_data(liste_temps,liste_T)
            line1.set_data(liste_temps,liste_T2)
            line2.set_data(liste_temps,liste_P)


            line = str(liste_temps[-1]) +'\t'+ str(liste_T[-1])+'\t'+ str(liste_T2[-1])+'\t'+ str(liste_P[-1])+'\n'
            lines.append(line)
            fichier = open('U:\Documents\data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte,indiquer le bon chemin
            return line0,line1,line2,


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
fig,(ax1,ax2,ax3) = plt.subplots(3,figsize=(10,10))
line0, = ax1.plot([],[])
line1, = ax2.plot([],[])
line2, = ax3.plot([],[])
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température 1 en °C')
ax1.axis([0,t_acquisition,0,Tmax])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('température 2 en °C')
ax2.axis([0,t_acquisition,0,Tmax])
ax3.set_xlabel('temps en s')
ax3.set_ylabel('Pression en Pa')
ax3.axis([0,t_acquisition,0.0,Pmax])




#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)


plt.show()


# plt.close(fig)
Data.close() # pour arrêter la lecture des données série




fig,(ax1,ax2,ax3) = plt.subplots(3,figsize=(10,10))
ax1.set_title('température 1=f(t)') # titre du graphique
ax1.scatter(liste_temps,liste_T, color ='r', marker = 'o') # On affiche les points de coordonnées (t,T) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([min(liste_temps),max(liste_temps),min(liste_T),max(liste_T)])  #limites pour les axes avec les valeurs extrêmes de temps et de température

ax2.set_title('température 2=f(t)') # titre du graphique
ax2.scatter(liste_temps,liste_T2, color ='r', marker = 'o') # On affiche les points de coordonnées (t,T) avec des points rouges
ax2.set_xlabel('temps en s')
ax2.set_ylabel('température en °C')
ax2.axis([min(liste_temps),max(liste_temps),min(liste_T2),max(liste_T2)])  #limites pour les axes avec les valeurs extrêmes de temps et de température


ax3.set_title('pression=f(t)') # titre du graphique
ax3.scatter(liste_temps,liste_P, color ='b', marker = 'o') # On affiche les points de coordonnées (t,P) avec des points bleus
ax3.set_xlabel('temps en s')
ax3.set_ylabel('Pression en Pa')
ax3.axis([min(liste_temps),max(liste_temps),min(liste_P),max(liste_P)])  #limites pour les axes avec les valeurs extrêmes de temps et de pression
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)










