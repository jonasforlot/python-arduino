

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt
# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte
lines = open('U:\Documents\essais Python\Alban pulse/data_arduino.txt').readlines() #on lit les lignes du fichier texte
open('data_new.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
data = np.loadtxt('data_new.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau

t = data[:,0] # selection de la premiere colonne
sign = data[:,1] # selection de la deuxieme colonne








# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure(1)
plt.scatter(t, sign, c = 'red', marker = '+')
plt.xlabel("t en s")
plt.ylabel("signal")
plt.show()



