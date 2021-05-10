

import matplotlib.pyplot as plt # pour les graphiques
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit
# importation des donnees txt obtenues apres pointage en supprimant la premiere ligne dans le fichier texte
lines = open('P:\Mes documents\essais Python\Améliorations\Données série PvapSat\data_arduinobis.txt').readlines() #on lit les lignes du fichier texte
open('P:\Mes documents\essais Python\Améliorations\Données série PvapSat\data_new.txt', 'w').writelines(lines[1:]) #création d'un nouveau fichier texte sans la première ligne
data = np.loadtxt('P:\Mes documents\essais Python\Améliorations\Données série PvapSat\data_new.txt')# importation du nouveau fichier texte pour récupérer les valeurs det, x et y dans un tableau

liste_temps = data[:,0] # selection de la premiere colonne
liste_T = data[:,1] # selection de la deuxieme colonne
liste_P = data[:,2] # selection de la deuxieme colonne




fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
line0, = ax1.plot([],[])
line1, = ax2.plot([],[])
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([0,500,0,120])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([0,500,0.0,120000])

ax1.set_title('température=f(t)') # titre du graphique
ax1.scatter(liste_temps,liste_T, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax1.set_xlabel('temps en s')
ax1.set_ylabel('température en °C')
ax1.axis([min(liste_temps),max(liste_temps),min(liste_T),max(liste_T)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température

ax2.set_title('pression=f(t)') # titre du graphique
ax2.scatter(liste_temps,liste_P, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
ax2.set_xlabel('temps en s')
ax2.set_ylabel('Pression en Pa')
ax2.axis([min(liste_temps),max(liste_temps),min(liste_P),max(liste_P)])  #limtes pour les axes avec les valeurs extrêmes de temps et de température
plt.show()  #afficher le


