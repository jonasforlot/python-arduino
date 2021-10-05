#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
import time # gestion du temps



#initialisation des listes
liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_masse = []

t_acquisition = 5.0


# Fonction pour la récupération des données série venant du port USB
def recup_port_usb() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port 
    return mData

Data =recup_port_usb()

# Essai pour une succession de 20 lignes de données
tempsreel=0
while tempsreel <= t_acquisition:
    line1 = Data.readline()
    print (line1)
    #on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)

    if len(listeDonnees)!= 0: # permet de nettoyer le flux de données acr seule une liste sur 3 contient des informations
        masse = float(listeDonnees[1].decode()) # après consulation des données, nous choisissons le 2ème élément de listeDonnees
        tempsmes = time.time()
        liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
        tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

        liste_masse.append(masse)
        print("m = %f"%(masse), " g") # affichage de la valeur de la masse
        liste_temps.append(tempsreel)
        print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
        print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0

Data.close()

plt.title('m=f(t)') # titre du graphique
plt.plot(liste_temps,liste_masse, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
plt.xlim (min(liste_temps),max(liste_temps))  #limtes pour les axes avec les valeurs extrêmes de I et de U
plt.ylim(min(liste_masse),max(liste_masse))
plt.xlabel('temps en s')
plt.ylabel('masse en g')
plt.show()