# -*- coding: utf-8 -*-
"""
Tracé de caractéristique et régression linéaire avec la fonction stats.linregress de scipy
"""

#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  ########################################################

import numpy as np  # numpy pour les maths , par exemple pour créer 256 valeurs régulièrement espacées entre 0 et 10 : np.linspace(0,10,256)
import matplotlib.pyplot as plt # pour les tracés de graphique


#########################################  LES VALEURS MESUREES DE I ET U SONT MISES DANS DES LISTES  ########################################################

I=[10.4,15.8,19.7,26.4,33.8,41.4,50.5,61.9,12.0,56.0] # Valeurs mesurées de I en mA
U=[1.255,1.92,2.378,3.174,4.075,4.99,6.1,7.46,2.100,6.190] # Valeurs mesurées de U en V
I= [elt/1000 for elt in I] # conversion de I en A (liste modifiée)

#################################   REGRESSION LINEAIRE ET TRACE DE GRAPHIQUE ########################################################################################

eq = np.polyfit (I,U,1) # pour faire la régression linéaire.
 # Pour un polynôme de degré 1, la fonction polyfit renvoie un tableau numpy contenant deux valeurs :   Les valeurs de ce tableau correspondent aux coefficients du polynôme modèle. La première valeur correspond au coefficient du terme de degré le plus élevé. Pour une droite, la première valeur correspond donc à son coefficient directeur et le second à son ordonnée à l’origine.

pente = eq[0] # pente
ordorig = eq[1] # ordonnée à l'origine


Xcalc = np.linspace(0,max(I) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = pente*Xcalc+ordorig # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
texte = 'equation de la droite  U = '+str(round(pente,3))+' I + '+str(round(ordorig,3)) # on affiche l'équation de la droite avec 3 décimales

print (texte)
plt.title('U=f(I)') # titre du graphique
plt.scatter(I,U, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
plt.plot(Xcalc,Ycalc,color = 'b',label = texte) # Affichage de la courbe modélisée en bleu
plt.xlabel('I en mA')       # nommer l'axe des abscisses
plt.ylabel('U en V')       # nommer l'axe des ordonnéees
plt.legend()   # pour afficher les légendes (label)
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)