"""
Tracé de vecteurs vitesse à partir du fichier txt d'un pointage video avec Latis Pro
on utlise np.loadtxt() de numpy pour récupérer les données mais il faut supprimer la première ligne du fichier txt, soit "à la main" soit ici directement dans le programme en créant un nouveau fichier texte data.txt
"""

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt

# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte (obtenu apres le pointage du mouvement parabolique sur Latis Pro)
lines = open('parabole_Latis_Pro.txt').readlines() #on lit les lignes du fichier texte
open('data.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
data = np.loadtxt('data.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau

t = data[:,0] # selection de la premiere colonne
x = data[:,1] # selection de la deuxieme colonne
y = data[:,3] # selection de la quatrieme colonne



# creation de listes vides pour les composantes des vitesses et acceleration
vx = []
vy = []


# boucle pour calcul de vx et vy et construction de fleches  a  partir de la methode annotate de la fonction pyplot (legendes sans texte)
for i in range(0,len(t)-1) :
    vx.append((x[i+1]-x[i])/(t[i+1]-t[i]))
    vy.append((y[i+1]-y[i])/(t[i+1]-t[i]))


    plt.quiver(x[i],y[i], vx[i], vy[i],color = 'r',width=0.005,scale=20,units='xy',angles='xy')
    #  méthode pour tracer des vecteurs

    # plt.annotate('', xy = (x[i]+vx[i-1]/20, y[i]+vy[i-1]/20), xytext = (x[i], y[i]), arrowprops = {'color' : 'r','width': 1, 'headwidth': 3})
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






