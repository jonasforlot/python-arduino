#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0

liste_t_mesure =[]

liste_T = [] # liste pour stocker les valeurs de température
liste_P = [] # liste pour stocker les valeurs de pression

t_acquisition = 100.0
Tmax= 110.0 # en °C
Pmax =140000.0 # en Pa

#Ecriture dans un fichier txt
lines=['t\tT\tP\n'] #première ligne du fichier txt
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


    if len(listeDonnees)== 7 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 3ème élément de listeDonnees
        # temp = float(listeDonnees[5].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        pression = float(listeDonnees[5].decode()) # après consulation des données, nous choisissons le 10ème élément de listeDonnees
        liste_t_mesure.append(temps)
        if liste_t_mesure[0]< 1 : # pour éventuellement éliminer les premières valeurs fausses de temps (défaut d'Arduino)
            while temps <= t_acquisition:
                # liste_T.append(temp)
                # print("Température = %f"%(temp)) # affichage de la valeur de la température
                liste_temps.append(temps)
                print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
                liste_P.append(pression)
                print("Pression = %f"%(pression)) # affichage de la valeur de la pression
                # line0.set_data(liste_temps,liste_T)
                line1.set_data(liste_temps,liste_P)

                line = str(liste_temps[-1]) +'\t'+ str(liste_P[-1])+'\n'
                lines.append(line)
                fichier = open('U:\Documents\data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte,indiquer le bon chemin
                return line1,
        else :
            del liste_t_mesure[0]









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
line1, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(0,Pmax)
plt.xlabel('temps en s')
plt.ylabel('pression en Pa')
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

plt.show()

plt.close(fig)
Data.close()

plt.title('d=f(t)') # titre du graphique
plt.plot(liste_temps,liste_P, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de I et de U
plt.ylim(min(liste_P),max(liste_P))
plt.xlabel('temps en s')
plt.ylabel('pression en Pa')
plt.show()