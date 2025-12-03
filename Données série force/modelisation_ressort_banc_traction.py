

# -*- coding: utf-8 -*-
"""
Tracé de la force en fonction de la position pour un ressort sur le banc de traction, et  régression linéaire avec la fonction stats.linregress de scipy
"""

#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  ########################################################

import numpy as np  # numpy pour les maths , par exemple pour créer 256 valeurs régulièrement espacées entre 0 et 10 : np.linspace(0,10,256)
import matplotlib.pyplot as plt # pour les tracés de graphique
from scipy import stats # module permettant de faire la régression linéaire à partir d'une liste X et d'une liste Y, stats.linregress(X,Y) renvoie 5 valeurs. Les 3 premières valeurs sont la pente, l'ordonnée à l'origine, et le coefficient de corrélation (à mettre au carré)

# importation des donnees txt obtenues avec le logiciel NovaControl
lines = open('donnees_banc_traction.txt').readlines() # ouverture du fichier texte
for i in range(len(lines)):                  # On remplace les virgules par des points pour les nombres décimaux
   lines[i]=lines[i].replace(',','.')

open('data.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
data = np.loadtxt('data.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau

x = data[:,1]*0.001 # selection de la deuxième colonne et conversion de la position en m
y = data[:,2]*9.81  # selection de la troisième colonne, force en N à partir de la tension mesurée



#################################   REGRESSION LINEAIRE ET TRACE DE GRAPHIQUE ########################################################################################

eq = stats.linregress (x,y) # pour faire la régression linéaire

pente = eq[0] # pente
ordorig = eq[1] # ordonnée à l'origine
coeff2 = eq[2]**2 # coefficient de corrélation au carré r²

Xcalc = np.linspace(0,max(x) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = pente*Xcalc+ordorig # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
texte = 'equation de la droite  F = '+str(round(pente,3))+' x + '+str(round(ordorig,3))+'     R² = '+str(round(coeff2,3)) # on affiche l'équation de la droite avec 3 décimales

print (texte)
plt.title('F=f(x)') # titre du graphique
plt.scatter(x,y, color ='r', marker = 'o') # On affiche les points de coordonnées (x, forceU) avec des points rouges
plt.plot(Xcalc,Ycalc,color = 'b',label = texte) # Affichage de la courbe modélisée en bleu
plt.xlabel('x en m')       # nommer l'axe des abscisses
plt.ylabel('F en N')       # nommer l'axe des ordonnéees
plt.legend()   # pour afficher les légendes (label)
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)