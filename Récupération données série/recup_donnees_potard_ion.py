#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps

#initialisation des listes

liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_tension = [] # liste pour stocker les valeurs de tension

t_acquisition = 10.0
Umax= 5.0 # en V


#pour le graphe en temps réel
def animate(i):
    
            line.set_data(liste_temps,liste_tension)
            return line,






# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description or 'CDC' in p.description  :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData

# Création figure
fig=plt.figure()
plt.xlabel('temps en s')
plt.ylabel('Tension en V')
plt.xlim(0, t_acquisition)
plt.ylim(0,Umax)
plt.show()

Data =recup_port_Arduino() #récupération des données


# Acquition temporelle
temps=0
while temps <= t_acquisition:
    line1 = Data.readline()
    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)
    
    if len(listeDonnees)== 6 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        U = float(listeDonnees[1].decode()) # après consulation des données, nous choisissons le 4ème élément de listeDonnees
        temps = (float(listeDonnees[4].decode()))/1000.0 # après consulation des données, nous choisissons le 2ème élément de listeDonnees

        liste_tension.append(U)
        print("U = %f"%(U)) # affichage de la valeur de la vitesse
        liste_temps.append(temps)
        print("temps mesuré = %f"%(temps), " s") # affichage de la valeur du temps absolu
        plt.plot(liste_temps,liste_tension, color ='r', marker = 'o') # On affiche les points de coordonnées (t,rps) avec des points rouges
        
        plt.draw()
        plt.pause(0.1)


Data.close()
plt.close()



   


   

# 
# 
# # #Animation
# # ani = animation.FuncAnimation(fig, animate, frames=200,  interval=20,repeat=False)
# 
# plt.show()
# 
# plt.close(fig)
# Data.close() # pour arrêter la lecture des données série



plt.title('Tension=f(t)') # titre du graphique
plt.scatter(liste_temps,liste_tension, color ='r', marker = 'o') # On affiche les points de coordonnées (t,rps) avec des points rouges

plt.xlabel('temps en s')
plt.ylabel('Tension en V')
plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de t et de rps
plt.ylim(min(liste_tension),max(liste_tension))
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)

#Ecriture dans un fichier txt
lines=['t\tU\n'] #première ligne du fichier txt
for i in range (len (liste_tension)):
    line = str(liste_temps[i]) +'\t'+ str(liste_tension[i])+'\n'
    lines.append(line)

fichier = open('/Users/jonasforlot/Documents/Python/Python Arduino/potard/recup_donnees_potard.py\data_arduino.txt', 'w').writelines(lines) #création d'un nouveau fichier texte, indiquer le chemin si nécessaire
