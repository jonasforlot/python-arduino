
# -*- coding: utf-8 -*-
"""
Petit module avec une fonction import_txt qui retourne directement les valeurs de t,x et y à partir duf ichier texte d'un pointage sur Latis Pro
"""

import numpy as np # numpy pour l'importation des donnees en format txt

# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte (obtenu apres le pointage du mouvement parabolique sur Latis Pro)
def import_txt(fichier):

    lines = open(fichier).readlines() #on lit les lignes du fichier texte
    open('data.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
    data = np.loadtxt('data.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau
    t = data[:,0] # selection de la premiere colonne
    x = data[:,1] # selection de la deuxieme colonne
    y = data[:,3] # selection de la quatrieme colonne

    return(t,x,y)


# test des fonctions
if __name__ == "__main__":

    # regclavier()

    valeurs = import_txt('parabole_Latis_Pro.txt')
    print(valeurs)


