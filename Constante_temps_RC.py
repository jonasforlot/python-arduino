""""
Détermination de la valeur de la capacité d'un condensateur à partir de la constante de temps d'un circuit RC, avec étude statistique
Ce script a été écrit par Cristophe BELLESSORT (académie de Normandie)
Mme Marie-Anne DEJOAN (académie de Guyane) a apporté quelques modifications
Le programme effectue N mesures successives de la capacité d'un condensateur, et propose ensuite une étude statistique.

Modifié le 05/01/2021 par Jonas FORLOT pour acquisition sur carte Arduino avec le langage Python (grâce a la bibliothèque nanpy)

-------------------------------------------------------------------------------
 """

# %%%%%%%%%%%%%%%%%%%%%%% Cette partie permet de charger des librairies utiles au programme %%%%%%%%%%%%%%%%%%%%%%%

from nanpy import SerialManager  # Utiliser par l’interpréteur python pour communiquer avec la carte Arduino
from nanpy import ArduinoApi     # Utilisation des services arduino.
import time
from scipy import *   # Importer la bibliothèque scipy, module qui concerne le calcul scientifique
from pylab import *   # Importer la bibliothèque pylab, qui permet d’utiliser de manière aisée les bibliothèques NumPy
                      # (calcul scientifique) et matplotlib (représentation graphique à 2D)

import matplotlib.pyplot as plt
import sys

# %%%%%%%%%%%%%%%%%%%%%%% Cette partie permet la communication avec la carte Arduino %%%%%%%%%%%%%%%%%%%%%%%

# Configuration de la communication avec la carte Arduino
connection = SerialManager(device='COM8') # Windows: Le numéro de port est celui utilisé par la carte. Il est identifiable avec l'application "arduino"" par le menu [Outils][Port].Arduino




try:
    a = ArduinoApi(connection=connection)     # Création de l'objet d'exploitation  arduino, toutes les instructions propres au langage arduino seront précédées par a.
except:
    print("La librairie nanpy n'a pas été téléversée dans la carte Arduino")
    sys.exit();

a.pinMode(2,a.OUTPUT) # Broche 2 déclarée comme sortie


R = 10000     # Valeur de la résistance R
N = 100      # Nombre de mesures de C
compteur =0   # Initialisation du Compteur de mesures
# Définition et mise à zéro des durées mesurées et intervenant dans le calcul de "tau"
tempsDebut = 0
tempsFin = 0



capa = [] # On crée 1 liste vide pour accueillir les données (N mesures de C)


# %%%%%%%%%%%%%%%%%%%%%%% DEBUT DE LA BOUCLE DU PROGRAMME %%%%%%%%%%%%%%%%%%%%%%%

while (compteur < N):

    compteur +=1      # Incrémente "compteur" de un

    print ('Décharge ...')           # Décharge du condensateur
    while (a.analogRead(0) > 0):     # Broche analogique utilisée  pour la mesure de la tension.
        a.digitalWrite(2, a.LOW)

    print ('Charge ...')             # Charge du condensateur
    tempsDebut = time.time ()        # Mémorisation du temps au début de l'alimentation du circuit RC

    while (a.analogRead(0) < 647):    # Tant que le niveau lu est inférieur à 647 i.e. 63.2% de la valeur numérique 1023
        a.digitalWrite(2, a.HIGH)     # On alimente le circuit RC avec une tension de 5V

    # Une fois sorti de la boucle on mesure tempsFin
    tempsFin = time.time()          # Durée écoulée depuis le début du lancement du programme
    tau = (tempsFin - tempsDebut)   # Calcul de tau exprimé en s
    C = (tau/R)*1e6                 # Calcul de C exprimé en micro Farad
    capa.append(C)
    print("n° ",compteur, "   C en uF : ", round(C,4))   #♦Affichage de tau avec 3 décimales

    if (compteur == N) :
        print("Fin des ",N," mesures")

#--------------------------- FIN DE LA BOUCLE DU PROGRAMME ---------------------------

## CALCUL DE LA MOYENNE + ECART TYPE + INCERTITUDE TYPE

n=len(capa) # Compte le nombre d'éléments présents dans le tableau à 1 dimension et l'affecte à la variable n
print('Nombre de mesures :', n)
print('Moyenne de C :',mean(capa),' uF') # Affiche la moyenne sur l'ensemble des mesures effectuées
s=std(capa, ddof = 1) # Calcul l'écart-type à n-1 (ou déviation standard au sens statistique) et l'affecte à la variable s
print('Ecart-type non biaisé pour la série de mesures de C :', s, 'uF') # Affiche l'écart-type non biaisé
U=s/sqrt(n) # Calcul de l'incertitude-type
print('Incertitude-type sur la mesure de C :', U, 'uF') # Affiche l'incertitude-type

## TRACE DES HISTOGRAMMES

figure("Capacité du condensateur") # Définit le nom de la figure
hist([capa],range=(min(capa),max(capa)),bins=30,edgecolor = 'blue')  # la fonction bins est associée
                                                                      # au nombre d'intervalles pour l'axe des abscisses

ylabel('Nb de mesures') # Définit le nom des ordonnées
legend(["Capacité en uF"]) # Définit la légende
show() # Affiche l'histogramme
