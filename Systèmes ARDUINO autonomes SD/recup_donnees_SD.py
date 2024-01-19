

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt
# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte
lines = open('C:/fichier.txt').readlines() #on lit les lignes du fichier texte, spécifier le chemin C:/fichier.txt par exemple
open('data_new.txt', 'w').writelines(lines) #création d'un nouveau fichier texte
data = np.loadtxt('data_new.txt')# importation du nouveau fichier texte pour récupérer les valeurs de t, et des autres colonnes de donnees dans un tableau

t = data[:,0] # selection de la premiere colonne
donnee = data[:,1] # selection de la deuxieme colonne

# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure(1)
plt.scatter(t, donnee, c = 'red', marker = '+')
plt.xlabel("t en s")
plt.ylabel("donnée récupérée")

plt.show()





