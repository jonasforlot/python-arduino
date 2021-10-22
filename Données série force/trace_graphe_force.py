#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import sys
import time # gestion du temps


#initialisation des listes

liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_force = [] # liste pour stocker les valeurs de force

t_acquisition = 10.0
Fmax= 20

#Ecriture dans un fichier txt
lines=['t\tF\n'] #première ligne du fichier txt

# Fonction pour la récupération des données série venant du périphérique
def recup_port_USB() :
    ports = list(serial.tools.list_ports.comports())
    if len(ports) != 0 :
        print (ports)
        for p in ports:
            if 'USB' in p.description :
                mData = serial.Serial(p.device,9600)
                print("le périphérique est connecté sur le port "+str(mData.name)) # Affiche et vérifie que le port est ouvert
                return mData
            else :
                print ("Pas de périphérique USB")
    else :
        print ("Pas de port actif")

def extract_val (donnee) :
    if donnee[4] == '1' :
        donnee = '-'+ donnee[10:12] +'.'+ donnee[12:14]

    elif donnee[4] == '0' :
        donnee = '' + donnee[10:12] +'.'+ donnee[12:14]

    return (float(donnee))









#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1
    chaine = ''
    for i in range (16) :
        line1 = Data.read()
        # print (line1)

        listeDonnees=[]
        if line1 != b'\x81' and  line1 != b'\x02' and line1 !=b'\x81':
            line2 =line1.decode()
            # print (line2)
            listeDonnees = line2.strip()
            listeDonnees = line2.split()
            # print (listeDonnees)
            if  len(listeDonnees)!=0 :
                chaine += listeDonnees[0]
    # print (chaine)
    chainebis = extract_val(chaine)
    # print (chainebis)

    force = chainebis # après consulation des données, nous choisissons le 2ème élément de listeDonnees
    tempsmes = time.time()
    liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
    tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

    while tempsreel <= t_acquisition:
        liste_force.append(force)
        print("F = %f"%(force), " N") # affichage de la valeur de la force
        liste_temps.append(tempsreel)
        print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
        print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0
        line0.set_data(liste_temps,liste_force)
        line = str(liste_temps[-1]) +'\t'+ str(liste_force[-1])+'\n'
        lines.append(line)
        fichier = open('U:\Documents\essais Python\Améliorations\Données série force\data_force.txt', 'w').writelines(lines) #création d'un nouveau fichier texte
        return line0,


Data =recup_port_USB() #récupération des données

# Création figure
fig=plt.figure()
line0, = plt.plot([],[])
plt.xlabel('temps en s')
plt.ylabel('Force en N')
plt.xlim(0, t_acquisition)
plt.ylim(-Fmax,Fmax)
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=20000,  interval=20,repeat=False)

plt.show()
Data.close()
plt.close(fig)







