
"""
Programme Python pour récupérer les donnnées d'un code Arduino permettant de tracer une caractéristique d'une photorésistance (ou autre capteur résistif).
Montage : Une tension de 5 V est appliquée aux deux points extrêmes d'un potentiomètre. On crée une alimentation variable en récupérant la tension entre le point milieu et la masse .
On applique cette tension à une association série photorésistance avec résistance connue (1 kohms)-. On fait mesurer par Arduino la tension aux bornes de la photorésistance et l'intensité parcourant le circuit I = (tension alim - tension photorésistance)/R.
"""

#########################################  IMPORTATION DES BIBLIOTHEQUES ET MODULES  ########################################################

import numpy   # numpy pour les maths , par exemple pour créer 256 valeurs régulièrement espacées entre 0 et 10 : np.linspace(0,10,256)
from time import sleep             # pour faire des "pauses" dans l'exécution du programme
import matplotlib.pyplot as plt # pour les graphiques


from scipy import stats # module permettant de faire la régression linéaire à partir d'une liste X et d'une liste Y, stats.linregress(X,Y) renvoie 5 valeurs. Les 3 premières valeurs sont la pente, l'ordonnée à l'origine, et le coefficient de corrélation (à mettre au carré)


import serial
import serial.tools.list_ports



#########################################  COMMUNICATION AVEC CARTE ARDUINO ET DEFINITION DES VARIABLES  #######################################################

#initialisation des listes
U=[]
I=[]
lines = ['I(mA)\tU(V)\n']



# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
        # if 'CDC' in p.description :    #pour les utilisateurs de mac
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port 
    return mData





#########################################  Récupération des données qu'on stocke dans des listes   ##############################################################################

Data =recup_port_Arduino() #récupération des données

while  len (U)<10 :
    line = Data.readline()  # Lit la ligne venant du port série.
    print (line)
    listeDonnees = line.strip()
    listeDonnees = line.split() # on sépare les données de la ligne  et on les stocke dans une liste
    print(listeDonnees)  # affichage de la liste obtenue.

    if len(listeDonnees)!=0: # extraction des données (valeurs d'intensité et tension)
        tension = float(listeDonnees[2].decode())
        courant = float(listeDonnees[5].decode())
        U.append(tension)
        print("U = %f"%(tension))
        I.append(courant)
        print("I = %f"%(courant))
        
    


Data.close()

I= [elt/1000 for elt in I] # conversion de I en A (liste modifiée)

eq = stats.linregress (I,U) # pour faire la régression linéaire

pente = eq[0] # pente
ordorig = eq[1] # ordonnée à l'origine
coeff2 = eq[2]**2 # coefficient de corrélation au carré r²

Xcalc = numpy.linspace(0,max(I) , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
Ycalc = pente*Xcalc+ordorig # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I

global texte
texte = 'equation de la droite  U = '+str(round(pente,3))+' I + '+str(round(ordorig,3))+'     R² = '+str(round(coeff2,3)) # on affiche l'équation de la droite avec 3 décimales

print (texte)

# Affichage du graphique
plt.title('U=f(I)') # titre du graphique
plt.scatter(I,U, color ='r', marker = 'o') # On affiche les points de coordonnées (I,U) avec des points rouges
plt.plot(Xcalc,Ycalc,color = 'b',label = texte) # Affichage de la courbe modélisée en bleu
plt.xlabel('I')       # nommer l'axe des abscisses
plt.ylabel('U')       # nommer l'axe des ordonnéees
plt.xlim (min(I),max(I))  #limtes pour les axes avec les valeurs extrêmes de I et de U
plt.ylim(min(U),max(U))
plt.legend()   # pour afficher les légendes (label)
plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
#
#
#
for i in range (len (I)):
    line = str(I[i]) +'\t'+ str(U[i])+'\n'
    lines.append(line)



open('data.txt', 'w').writelines(lines) #création d'un nouveau fichier texte sans la première ligne
