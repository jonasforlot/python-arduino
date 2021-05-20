#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_rps = [] # liste pour stocker les valeurs de vitesse

t_acquisition = 10.0
rpsmax= 150 # en mm


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
        rps = float(listeDonnees[3].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        temps = (float(listeDonnees[1].decode()))/1000.0 # après consulation des données, nous choisissons le 2ème élément de listeDonnees


        while temps <= t_acquisition:
            liste_rps.append(rps)
            print("rps = %f"%(rps)) # affichage de la valeur de la vitesse
            liste_temps.append(temps)
            print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
            line.set_data(liste_temps,liste_rps)
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
plt.ylim(0,rpsmax)
plt.xlabel('temps en s')
plt.ylabel('rps')
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)

plt.show()

plt.close(fig)
Data.close() # pour arrêter la lecture des données série



plt.title('rps=f(t)') # titre du graphique
plt.scatter(liste_temps,liste_rps, color ='r', marker = 'o') # On affiche les points de coordonnées (t,rps) avec des points rouges
plt.xlabel('temps en s')
plt.ylabel('rps')
plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de t et de rps
plt.ylim(min(liste_rps),max(liste_rps))
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)

#Ecriture dans un fichier txt
lines=['t\trps\n'] #première ligne du fichier txt
for i in range (len (liste_rps)):
    line = str(liste_temps[i]) +'\t'+ str(liste_rps[i])+'\n'
    lines.append(line)

fichier = open('data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte, indiquer le chemin si nécessaire

