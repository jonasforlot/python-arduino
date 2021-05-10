#-------------------------------------------------------------------------------
# Name:        Elab_PA_niv1
# Purpose:     Programme d'utilisation du capteur de pression absolue Eurosmart Elab_PA.
#              Ce capteur permet de mesurer une pression de 200hPa à 4000hPa.
#              Le capteur utilise une broche analogique de la carte EDUCA DUINO Lab.
#              Les mesures effectuées sont transmises sur la console python.
# Author:      cletourneur
#
# Created:     30/01/2019
# Copyright:   (c) cletourneur 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from nanpy import SerialManager     # Utiliser par l'interpreteur python pour communiquer
                                    # avec la carte EDUCA DUINO LAB
from nanpy import ArduinoApi        # Utilisation des services arduino.

from eurosmart import *             # Utilisation de la librairie Eurosmart pour piloter le capteur Elab_PA

import time
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée

import sys

# Configuration de la communication avec la carte EDUCA DUINO Lab
portCom = detectePortComEducaDuinoLab()             # Disponible dans la librairie Eurosmart.
if ('none' == portCom):
    print('Pas de carte EDUCA DUINO LAB connectée au PC')
    sys.exit();

connection = SerialManager(device=portCom)          # Numéro de port utilisé par la carte.
#connection = SerialManager(device='COM28')         # Windows: Le numéro de port est celui utilisé par la carte. Il est identifiable avec l'application "arduino"" par le menu [Outils][Port].

try:
    arduino = ArduinoApi(connection=connection)     # Création de l'objet d'exploitation la librairie arduino
except:
    print("La librairie nanpy n'a pas été téléversée dans la carte EDUCA DUINO LAB")
    sys.exit();
eurosmart= Eurosmart(connection=connection)  # Création de l'objet d'utilisation des capteurs Eurosmart.

#initialisation des listes
liste_temps_mesure =[] # liste pour stocker le temps"brut"
liste_temps=[] # liste pour stocker les valeurs de temps en partant de t=0
liste_T = [] # liste pour stocker les valeurs de température
liste_P = [] # liste pour stocker les valeurs de température

t_acquisition = 1000.0
Tmax= 110.0 # en °C
Pmax =140000.0 # en Pa


# Définition des broches analogiques utilisées par le capteur Elab_PA.
_NUMER0_BROCHE_ANALOGIQUE = arduino.A8  # Broche analogique utilisée par le capteur pour la mesure de la tension. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).

def convertiValeurMesureAnalogiqueEnTension(_valeurAnalogique):
    """
    Converti la valeur analogique en tension.
    La valeur analogique va de 0 à 1023.
    La valeur tension va de 0 à 5V.
    """
    # La fonction de conversion valeur numérique/tension est de la forme tension = a * valeurNumerique.
    _VALEUR_NUMERIQUE_MIN= 0;
    _VALEUR_TENSION_MIN  = 0.0;
    _VALEUR_NUMERIQUE_MAX= 1023;   # convertisseur 10bits
    _VALEUR_TENSION_MAX  = 5.0;

    # Calcul du coefficient directeur
    a = (_VALEUR_TENSION_MAX-_VALEUR_TENSION_MIN)/(_VALEUR_NUMERIQUE_MAX-_VALEUR_NUMERIQUE_MIN);
    # Calcul de la tension
    tension_V= a * _valeurAnalogique;
    return(tension_V);
    pass

def convertiTensionEnPression(_tension):
    """
    Converti la valeur de tension en une valeur de pression.
    On mesure une tension de 0V pour une pression de 200hPa. (20000Pa)
    On mesure une tension de 5V pour une pression de 4000hPa (400000Pa)
    """

    # La fonction de conversion tension vers pression est de la forme pression = a * tension +b
    _VALEUR_PRESSION_MIN= 200.0;
    _VALEUR_TENSION_MIN = 0.0;
    _VALEUR_PRESSION_MAX= 4000.0; # 4000hPa
    _VALEUR_TENSION_MAX = 5.0;
    # Calcul du coefficient directeur
    a = (_VALEUR_PRESSION_MAX-_VALEUR_PRESSION_MIN)/(_VALEUR_TENSION_MAX-_VALEUR_TENSION_MIN);
    # Calcul du coefficient décalage à l'origine.
    b = _VALEUR_PRESSION_MAX - a * _VALEUR_TENSION_MAX;
    #calcul de la pression
    pression_hPa = (a * _tension) + b;    # Pression en hecto Pascal.
    pression_Pa = pression_hPa * 100;     # Conversion de hPa en Pa.
    return(pression_Pa);
    pass

def main():

    #pour le graphe en temps réel
    def animate(i):

        # Lecture de la valeur du capteur sur l'entree analogique.
        valeurNumerique=arduino.analogRead(_NUMER0_BROCHE_ANALOGIQUE)     # valeur comprise entre 0 et 1023.
        # Calcul de la tension fournie par le capteur.
        tension_V   = convertiValeurMesureAnalogiqueEnTension(valeurNumerique);
        # Calcul de la pression corespondant à la tension calculée.
        pression_Pa = convertiTensionEnPression(tension_V);

        valeurNumerique2=arduino.analogRead(arduino.A0)
        tension_V_T = convertiValeurMesureAnalogiqueEnTension(valeurNumerique2);
        temp_degreC = tension_V_T*100
        #Affichage des resultats sur la console Python
        print('Pression absolue:', '%.0f' %(pression_Pa), 'Pa' # Transmission de la pression en Pa
            )
        print('Temperature:', '%.0f' %(temp_degreC), '°C' # Transmission de la pression en Pa
            )
        tempsmes = time.time()
        liste_temps_mesure.append(tempsmes) # temps mesuré "brut" stocké dans une liste
        tempsreel = tempsmes - liste_temps_mesure[0] # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)


        while tempsreel <= t_acquisition:
            liste_T.append(temp_degreC)
            print("Température = %f"%(temp_degreC)) # affichage de la valeur de la distance
            liste_temps.append(tempsreel)
            print("temps mesuré = %f"%(tempsreel), " s") # affichage de la valeur du temps absolu
            liste_P.append(pression_Pa)
            print("Pression = %f"%(pression_Pa)) # affichage de la valeur de la distance
            line0.set_data(liste_temps,liste_T)
            line1.set_data(liste_temps,liste_P)

            return line0,line1,

    # Création figure
    fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
    line0, = ax1.plot([],[])
    line1, = ax2.plot([],[])
    ax1.set_xlabel('temps en s')
    ax1.set_ylabel('température en °C')
    ax1.axis([0,t_acquisition,0,Tmax])
    ax2.set_xlabel('temps en s')
    ax2.set_ylabel('Pression en Pa')
    ax2.axis([0,t_acquisition,0.0,Pmax])




    #Animation
    ani = animation.FuncAnimation(fig, animate, frames=4000,  interval=20,repeat=False)

    plt.show()

    # plt.close(fig)



    fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
    line0, = ax1.plot([],[])
    line1, = ax2.plot([],[])
    ax1.set_xlabel('temps en s')
    ax1.set_ylabel('température en °C')
    ax1.axis([0,t_acquisition,0,Tmax])
    ax2.set_xlabel('temps en s')
    ax2.set_ylabel('Pression en Pa')
    ax2.axis([0,t_acquisition,0.0,Pmax])

    ax1.set_title('température=f(t)') # titre du graphique
    ax1.scatter(liste_temps,liste_T, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
    ax1.set_xlabel('temps en s')
    ax1.set_ylabel('température en °C')
    ax1.axis([min(liste_temps),max(liste_temps),min(liste_T),max(liste_T)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température

    ax2.set_title('pression=f(t)') # titre du graphique
    ax2.scatter(liste_temps,liste_P, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
    ax2.set_xlabel('temps en s')
    ax2.set_ylabel('Pression en Pa')
    ax2.axis([min(liste_temps),max(liste_temps),min(liste_P),max(liste_P)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température
    plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
    #Ecriture dans un fichier txt
    lines=['t\tT\tP\n'] #première ligne du fichier txt
    for i in range (len (liste_T)):
        line = str(liste_temps[i]) +'\t'+ str(liste_T[i])+'\t'+ str(liste_P[i])+'\n'
        lines.append(line)

    fichier = open('P:\Mes documents\essais Python\Améliorations\Données série PvapSat\data_arduino_nanpyk.txt', 'w').writelines(lines) #création d'un nouveau fichier texte

    pass

if __name__ == '__main__':
    main()
