# Réglage balance : RS232 -> baud 9600, parity 8 no
#                   Print ->  a.print continu, content-> numbers on
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
liste_masse = [] # liste pour stocker les valeurs de masse

t_acquisition = 10.0
mmax= 700

#Ecriture dans un fichier txt
lines=['t\tm\n'] #première ligne du fichier txt

# Fonction pour la récupération des données série venant de la carte Arduino
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
                print ("Pas de carte Arduino détectée")
    else :
        print ("Pas de port actif")







#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1
    chaine = ''
    for i in range (13) :
        line1 = Data.read()
        print (line1)

        listeDonnees=[]

        line2 =line1.decode()
        # print (line2)
        listeDonnees = line2.strip()
        listeDonnees = line2.split()
        # print (listeDonnees)
        if  len(listeDonnees)!=0 :
            chaine += listeDonnees[0]
    print (chaine)
    # chainebis = extract_val(chaine)
    # print (chainebis)

    masse = float(chaine)
    tempsmes = time.time()
    liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
    tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)

    while tempsreel <= t_acquisition:
        liste_masse.append(masse)
        print("m = %f"%(masse), " g") # affichage de la valeur de la force
        liste_temps.append(tempsreel)
        print("temps mesuré = %f"%(tempsmes), " s") # affichage de la valeur du temps absolu
        print("temps réel= %f"%(tempsreel), " s") # affichage de la valeur du temps en partant de 0
        line0.set_data(liste_temps,liste_masse)
        line = str(liste_temps[-1]) +'\t'+ str(liste_masse[-1])+'\n'
        lines.append(line)
        fichier = open('U:\Documents\essais Python\Améliorations\\data_balance.txt', 'w').writelines(lines) #création d'un nouveau fichier texte
        return line0,


Data =recup_port_USB() #récupération des données

# Création figure
fig=plt.figure()
line0, = plt.plot([],[])
plt.xlabel('temps en s')
plt.ylabel('masse en g')
plt.xlim(0, t_acquisition)
plt.ylim(0,mmax)
plt.grid()


#Animation
ani = animation.FuncAnimation(fig, animate, frames=20000,  interval=20,repeat=False)

plt.show()
Data.close()
plt.close(fig)







