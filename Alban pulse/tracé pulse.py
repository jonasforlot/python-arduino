
#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import time # gestion du temps


#initialisation des listes


liste_t_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_signal = [] # liste pour stocker les valeurs de concentration


t_acquisition = 10.0
mmax= 1023 # en g
mmin =0




#pour le graphe en temps réel
def animate(i):
    line1 = Data.readline()
    print (line1)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)




    if len(listeDonnees)== 2 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        signal = float(listeDonnees[1].decode()) # après consulation des données, nous choisissons le 2ème élément de listeDonnees
        temps = float(listeDonnees[0].decode())/1000.0 # après consulation des données, nous choisissons le 2ème élément de listeDonnees
        liste_t_mesure.append(temps)
        if liste_t_mesure[0]< 1 : # pour éventuellement éliminer les premières valeurs fausses de temps (défaut d'Arduino)
            while temps <= t_acquisition:
                liste_signal.append(signal)
                liste_temps.append(temps)
                print("%5.3f"%(temps), " s \t | \t %f"%(signal))
                line.set_data(liste_temps,liste_signal)
                return line,
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
line, = plt.plot([],[])
plt.xlim(0, t_acquisition)
plt.ylim(mmin,mmax)
plt.xlabel('temps en s')
plt.ylabel('signal en g')
plt.grid()




#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)


plt.show()


plt.close(fig)
Data.close() # pour arrêter la lecture des données série


#Ecriture dans un fichier txt
lines=['t\tm\n'] #première ligne du fichier txt
for i in range (len (liste_signal)):
    line = str(liste_temps[i]) +'\t'+ str(liste_signal[i])+'\n'
    lines.append(line)


fichier = open('data_arduino.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte