# -*- coding: utf-8 -*-
"""
test du module regression
"""


import numpy as np  # numpy pour les maths , par exemple pour la racine carrée, il faut écrire np.sqrt
import matplotlib.pyplot as plt
from regression import *



I=[10.4,15.8,19.7,26.4,33.8,41.4,50.5,61.9,12.0,56.0]
U=[1.255,1.92,2.378,3.174,4.075,4.99,6.1,7.46,2.100,6.190]

M=np.array([I,U])
M1 =np.transpose(M)
print (M1)
np.savetxt('donnees.txt',M1)

############################ Régression linéaire sans et avec élimination de points  ######################################################
equation = reglin(I,U,'I','U')


Xcalc = np.linspace(0,max(I) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = valeurs_calc(Xcalc,I,U) # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
plt.subplot(1, 2, 1)
plt.title('U=f(I)')
plt.scatter(I,U, color ='r', marker = 'o')
plt.plot(Xcalc,Ycalc,color = 'b',label = equation)
plt.xlabel('I')       #nommer l'axe des abscisses#
plt.ylabel('U')       #nommer l'axe des ordonnéees#
plt.legend()   # pour afficher les légendes (label)



equation = reglin_avec_elimination(I,U,'I','U')
(I,U) = elimination_valeurs (I,U)# création des nouvelles listes après élimination de points

Xcalc = np.linspace(0,max(I) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = valeurs_calc(Xcalc,I,U) # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
plt.subplot(1, 2, 2)
plt.title('U=f(I) avec élimination')
plt.scatter(I,U, color ='r', marker = 'o')
plt.plot(Xcalc,Ycalc,color = 'b',label = equation)
plt.xlabel('I')       #nommer l'axe des abscisses#
plt.ylabel('U')       #nommer l'axe des ordonnéees#
plt.legend()   # pour afficher les légendes (label)
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
tableur (I,U,'I','U','A','V')


################# Régression linéaire avec saisie clavier  ENLEVER LES HACHTAGS POUR LE TEST (CTRL+T en sélectionnant les lignes )###################
# regclavier()


################# Régression linéaire avec saisie clavier avec élimination ENLEVER LES HACHTAGS POUR LE TEST (CTRL+T en sélectionnant les lignes) ###################
# regclavier_avec_elimination()