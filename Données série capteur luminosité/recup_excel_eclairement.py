import numpy as np
import os
import pandas as pd

# Initialisation des listes pour stocker les colonnes de temps et éclairement
time_column = None
eclairement_columns = []

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

    # Sauvegarder la première colonne de temps seulement à partir du premier fichier
    if time_column is None:
        time_column = t

    # Ajouter la colonne d'éclairement à la liste
    eclairement_columns.append(ecl)

    compteur += 1

# Conversion des colonnes d'éclairement en array numpy pour les assembler
eclairement_array = np.column_stack(eclairement_columns)

# Création du DataFrame en ajoutant la colonne de temps et les colonnes d'éclairement
df = pd.DataFrame(eclairement_array, columns=[f'Eclairement_{i}' for i in range(compteur)])
df.insert(0, 'Temps', time_column)  # Insérer la colonne de temps au début

# Sauvegarde du fichier Excel
df.to_excel('eclairement_data.xlsx', index=False)

print("Fichier Excel créé : eclairement_data.xlsx")
