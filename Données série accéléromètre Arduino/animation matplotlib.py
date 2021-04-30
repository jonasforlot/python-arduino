import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation




TWOPI = 2*np.pi


liste_compt = [0]
liste_etat_new = [False]
liste_etat_old = [False]
fig, ax = plt.subplots()
compt = 0
etat_old = False
etat_new = False
t = np.arange(0.0, 4*TWOPI, 0.001)
s = np.sin(t+0.2)+0.8
s1 = np.sin(t+0.2)

l = plt.plot(t, s)
m = plt.plot(t, s-s1,"r--")

# ax = plt.axis([0,2*TWOPI,-2,2])

tex = 'Compteur'
redDot, = plt.plot([0], [np.sin(0)], 'ro')
compteur_text = ax.text(0, 0.3, tex, fontsize=15, va='bottom')
comptage_text = ax.text(0, 0.05, '', fontsize=15, va='bottom')
periode_text = ax.text(4, 0.95, 'Période', fontsize=15, va='bottom',color = 'green')
ax.annotate ('', (2.85, 0.9), (9.35, 0.9), arrowprops={'color':'g','arrowstyle':'<->'})
def comptage(x):


    if  x < 0.8 :
        liste_etat_new[-1] = True
    else :
        liste_etat_new[-1] = False
    if liste_etat_old[-1] != liste_etat_new[-1] :
        liste_etat_old[-1] = liste_etat_new[-1]
        liste_compt[-1]+=1
    return liste_compt[-1]



def animate(i):
    curseur = np.sin(i+0.2)+0.8


    print (curseur)

    compteur = comptage(curseur)

    comptage_text.set_text(compteur)
    redDot.set_data(i, curseur)
    return redDot, comptage_text

# create animation using the animate() function
myAnimation = animation.FuncAnimation(fig, animate, frames=np.arange(0.0, 4*TWOPI, 0.1), \
                                      interval=100, blit=True, repeat=False)

plt.show()