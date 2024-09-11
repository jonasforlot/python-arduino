import matplotlib.pyplot as plt
import numpy as np
import os

# Initialisation du graphique
plt.figure()

# Boucle pour traiter les fichiers eclairement0.txt, eclairement1.txt, etc.
compteur = 0
while os.path.exists(f"eclairement{compteur}.txt"):
    # Lecture du fichier correspondant
    lines = open(f'eclairement{compteur}.txt').readlines()
    open(f'data_new{compteur}.txt', 'w').writelines(lines[1:])  # Supprimer la première ligne

    # Charger les données
    data = np.loadtxt(f'data_new{compteur}.txt')
    t = data[:, 0]  # Temps (colonne 1)
    ecl = data[:, 1]  # Éclairement (colonne 2)

    # Tracer la courbe pour chaque fichier avec un label correspondant
    plt.scatter(t, ecl, marker='+')
    plt.plot(t, ecl, label=f'Eclairement fichier {compteur}')

    compteur += 1

# Configuration du graphique
plt.xlabel("Temps en s")
plt.ylabel("Eclairement en lux")
plt.title('Eclairement en fonction du temps')
plt.legend()  # Afficher les légendes

# Sauvegarde de la figure en PDF
plt.savefig('eclairement_multi.pdf')

# Affichage de la figure
plt.show()

