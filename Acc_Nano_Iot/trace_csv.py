

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt
# Nom du fichier d'entrée et de sortie
fichier_entree = "mySet.csv"
fichier_sortie = "mySet_sans_3_dernieres_colonnes.csv"

# Ouvrir le fichier d'entrée en mode lecture
with open(fichier_entree, mode='r') as f_entree:
	lignes = f_entree.readlines()

# Ouvrir le fichier de sortie en mode écriture
with open(fichier_sortie, mode='w') as f_sortie:
	for ligne in lignes:
	# Divisez la ligne en colonnes en utilisant la tabulation comme délimiteur
		colonnes = ligne.strip().split('\t')
	# Supprimez les trois dernières colonnes
		nouvelles_colonnes = colonnes[:-3]
		# Recréez la ligne en joignant les colonnes avec des tabulations
		nouvelle_ligne = '\t'.join(nouvelles_colonnes) + '\n'
		# Écrire la ligne modifiée dans le fichier de sortie
		f_sortie.write(nouvelle_ligne)


data = np.genfromtxt(fichier_sortie, delimiter='\t', skip_header=1)

t = data[:,0] # selection de la premiere colonne
acc1 = data[:,1] # selection de la deuxieme colonne





# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure(1)
plt.title("Accélération selon x en fonction du temps")
plt.plot(t, acc1, c = 'red', marker = '+',label='Acc1')

plt.xlabel("t en s")
plt.ylabel("a en g")
plt.legend()

plt.show()



