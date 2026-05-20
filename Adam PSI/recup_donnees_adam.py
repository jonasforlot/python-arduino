#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps


#initialisation des listes


liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_rps1 = [] # liste pour stocker les valeurs de température
liste_rps2 = [] # liste pour stocker les valeurs de pression


t_acquisition = 10.0
rps1max= 100
rps2max =100

#Ecriture dans un fichier txt
lines=['t\trps1\trps2\n'] #première ligne du fichier txt
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




    if len(listeDonnees)== 6 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = (float(listeDonnees[1].decode()))/1000.0 # après consulation des données, nous choisissons le 3ème élément de listeDonnees
        rps1 = float(listeDonnees[3].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        rps2 = float(listeDonnees[5].decode()) # après consulation des données, nous choisissons le 10ème élément de listeDonnees


        while temps <= t_acquisition:
            liste_rps1.append(rps1)
            print("rps1 = %f"%(rps1)) # affichage de la valeur de la température
            liste_temps.append(temps)
            print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
            liste_rps2.append(rps2)
            print("rps2 = %f"%(rps2)) # affichage de la valeur de la pression
            line0.set_data(liste_temps,liste_rps1)
            line1.set_data(liste_temps,liste_rps2)


            line = str(liste_temps[-1]) +'\t'+ str(liste_rps1[-1])+'\t'+ str(liste_rps2[-1])+'\n'
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
ax1.set_ylabel('rps1')
ax1.axis([0,t_acquisition,0,rps1max])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('rps2')
ax2.axis([0,t_acquisition,0.0,rps2max])




#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)


plt.show()


# plt.close(fig)
Data.close() # pour arrêter la lecture des données série




fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
ax1.set_title('rps1=f(t)') # titre du graphique
ax1.scatter(liste_temps,liste_rps1, color ='r', marker = 'o') # On affiche les points de coordonnées (t,rps1) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('rps1')
ax1.axis([min(liste_temps),max(liste_temps),min(liste_rps1),max(liste_rps1)])  #limites pour les axes a

ax2.set_title('rps2=f(t)') # titre du graphique
ax2.scatter(liste_temps,liste_rps2, color ='b', marker = 'o') # On affiche les points de coordonnées (t,rps2) avec des points bleus
ax2.set_xlabel('temps en s')
ax2.set_ylabel('rps2')
ax2.axis([min(liste_temps),max(liste_temps),min(liste_rps2),max(liste_rps2)])  #limites pour les axes
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
