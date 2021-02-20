# -*- coding: utf-8 -*-
"""
Tracé de vecteurs vitesse à partir du fichier txt d'un pointage video avec Latis Pro
on utlise la fonction import_txt du module import_latis (fichier module "maison" à mettre dans le même dossier)qui retourne directement t,x et y
"""

import matplotlib.pyplot as plt # pour les graphiques
from import_latis import * #  pour l'importation des donnees en format txt

# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte (obtenu apres le pointage du mouvement parabolique sur Latis Pro)

t,x,y = import_txt('parabole_Latis_Pro.txt')# importation du nouveau fichier texte pour récupérer dans des listes les valeurs de t, x et y




# creation de listes vides pour les composantes des vitesses et acceleration
vx = []
vy = []


# boucle pour calcul de vx et vy et construction de fleches  a  partir de la methode annotate de la fonction pyplot (legendes sans texte)
for i in range(0,len(t)-1) :
    vx.append((x[i+1]-x[i])/(t[i+1]-t[i]))
    vy.append((y[i+1]-y[i])/(t[i+1]-t[i]))


    # plt.quiver(x[i],y[i], vx[i], vy[i],color = 'r',width=0.005,scale=20,units='xy',angles='xy')
    #  méthode pour tracer des vecteurs

    plt.annotate('', xy = (x[i]+vx[i-1]/20, y[i]+vy[i-1]/20), xytext = (x[i], y[i]), arrowprops = {'color' : 'r','width': 1, 'headwidth': 3})
    # autre méthode pour tracer des vecteurs : xytext donne les coordonnees du debut de la fleche, xy donne les coordonnnees de la pointe de la fleche

    # plt.arrow(x[i],y[i], vx[i]/20, vy[i]/20,length_includes_head=True,color = 'r',width=0.005)
    # 3ème méthode pour tracer des vecteurs

# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure(1)
plt.scatter(x, y, c = 'red', marker = '+')
plt.suptitle (" Représentation de $y=f(x)$  " )
plt.title (" Tracé des vecteurs vitesse  " )
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.show()





