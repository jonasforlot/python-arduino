

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit
# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte 
lines = open('data_accelerometre.txt').readlines() #on lit les lignes du fichier texte
open('data_new.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
data = np.loadtxt('data_new.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau

t = data[:,0] # selection de la premiere colonne
acc = data[:,1] # selection de la deuxieme colonne


def estim_freq(y) : 
    compt = 0
    moy = np.mean(y)
    etat_old = False
    etat_new = False
    for i in range (len(y)) :
        if  y[i] < moy :
            etat_new = True
        else :
            etat_new = False
        if etat_old != etat_new :
            etat_old = etat_new
            compt += 1

    return (compt/(2*10.0)) #temps d'acquisition de 10s

# Fonction d'estimation des valeurs des paramètres de la modélisation
def get_p0(x, y): 
    
    A0 = (np.max(y)-np.min(y))/2
    f0 =estim_freq(y)
    phase0 =0
    offset0 = np.mean(y)
    return [A0, f0, phase0,offset0]

def f(x,a,b,c,d):
	return (a*np.sin(2.*np.pi*b*x+c)+d)
# 
# popt,pcov = curve_fit (f,t,acc)
popt,pcov = curve_fit (f,t,acc,p0=get_p0(t,acc))

texte = 'Accélération = '+str(round(float(popt[0]),2))+' sin (2pi*'+str(round(float(popt[1]),2))+'*t+'+str(round(float(popt[2]),2))+') + '+str(round(float(popt[3]),2))+'\n' +'A = '+str(round(float(popt[0]),2))+'; f = '+str(round(float(popt[1]),2))+' ; phase ='+str(round(float(popt[2]),2))+' ; offset = '+str(round(float(popt[3]),2))

# afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
plt.figure(1)
plt.plot(t, acc, c = 'red', marker = '+')
plt.plot(t,f(t,*popt),'g--',label = texte)
plt.xlabel("t en s")
plt.ylabel("a en g")
plt.legend()   # pour afficher les légendes (label)
plt.show()


print (texte)
print(get_p0(t,acc))
estim_freq(acc)


