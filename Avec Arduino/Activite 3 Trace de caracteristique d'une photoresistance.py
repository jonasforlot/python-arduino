# -*- coding: utf-8 -*-
"""
Programme Python pour tracé caractéristique d'une photorésistance (ou autre capteur résistif).
Une tension de 5 V est appliquée aux deux points extrêmes d'un potentiomètre. On crée une alimentation variable en récupérant la tension entre le point milieu et la masse .
On applique cette tension à une association série photorésistance avec résistance connue (220, ohms)-. On fait mesurer par Arduino la tension aux bornes de la photorésistance et l'intensité parcourant le circuit I = (tension alim - tension photorésistance)/R.
"""

#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  ########################################################
from nanpy import ArduinoApi        # importation des bibliothèques pour communication avec Arduino
from nanpy import SerialManager

import numpy as np  # numpy pour les maths , par exemple pour créer 256 valeurs régulièrement espacées entre 0 et 10 : np.linspace(0,10,256)
from time import sleep             # pour faire des "pauses" dans l'exécution du programme
import matplotlib.pyplot as plt # pour les graphiques

from scipy import stats # module permettant de faire la régression linéaire à partir d'une liste X et d'une liste Y, stats.linregress(X,Y) renvoie 5 valeurs. Les 3 premières valeurs sont la pente, l'ordonnée à l'origine, et le coefficient de corrélation (à mettre au carré)


#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES BROCHES ET VARIABLES  #######################################################

R= 1000.0 # valeur de résistance connue pour mesure de l'intensité
connection = SerialManager(device='COM29') #renseigner le bon port utilisé par la carte Arduino

a = ArduinoApi(connection=connection) #connection à la carte Arduino, on précédera chaque instruction Arduino par a. (exemple a.pinMode(2,a.OUTPUT)


broche_LDR = 0 #Tension aux bornes de la photorésistance, selon la version de nanpy il faut indiquer 0 ou A.0
broche_alim =1 # Tension entre le point milieu du potentiomètre et la masse (tension de l'alimentation variable), selon la version de nanpy il faut indiquer 1 ou A.1

U=[]
I=[]
U_alim = 0.0
courant_A =0.0


#########################################  ACQUISITION  AVEC ARDUINO EN LANGAGE PYTHON     ##############################################################################

while U_alim < 5.0 : # on agit sur le potentiomètre pour faire varier la tension U_alim de 0 à 5V, une mesure sera faite toutes les 2 secondes. Dès que la tension maximale est atteinte, le programme s'arrête

    Valeur_alim = a.analogRead(broche_alim) # lecture de la tension U_LDR par la carte Arduino (valeur comprise entre 0 et 1023)
    U_alim = float(Valeur_alim *5.0/1023) # conversion pour récupérer la valeur de la tension

    Valeur_LDR   = a.analogRead(broche_LDR) # lecture de la tension U_alim par la carte Arduino (valeur comprise entre 0 et 1023)
    U_LDR_mesure = float(Valeur_LDR*5.0/1023) # conversion pour récupérer la valeur de la tension

    courant_A   = (U_alim - U_LDR_mesure)/R # pour récupérer la valeur de l'intensité du courant dans le circuit (loi d'Ohm)
    I.append(courant_A) # On  met la valeur de l'intensité dans la liste I
    U.append (U_LDR_mesure) # On  met la valeur de la tension U_LDRdans la liste U

    print ('I :',I)
    print('U photorésistance : ',U) # pour afficher les listes au fur et à mesure de l'acqusition
    sleep(2)

#################################   REGRESSION LINEAIRE ET TRACE DE GRAPHIQUE ########################################################################################
eq = stats.linregress (I,U) # pour faire la régression linéaire

pente = eq[0] # pente
ordorig = eq[1] # ordonnée à l'origine
coeff2 = eq[2]**2 # coefficient de corrélation au carré r²

Xcalc = np.linspace(0,max(I) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = pente*Xcalc+ordorig # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
texte = 'equation de la droite  U = '+str(round(pente,3))+' I + '+str(round(ordorig,3))+'     R² = '+str(round(coeff2,3)) # on affiche l'équation de la droite avec 3 décimales

print (texte)

plt.title('U=f(I)') # titre du graphique
plt.scatter(I,U, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
plt.plot(Xcalc,Ycalc,color = 'b',label = texte) # Affichage de la courbe modélisée en bleu
plt.xlabel('I')       # nommer l'axe des abscisses
plt.ylabel('U')       # nommer l'axe des ordonnéees
plt.xlim (min(I),max(I))  #limtes pour les axes avec les valeurs extrêmes de I et de U
plt.ylim(min(U),max(U))
plt.legend()   # pour afficher les légendes (label)
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)