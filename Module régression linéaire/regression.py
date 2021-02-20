# -*- coding: utf-8 -*-
"""
module regression
"""


import numpy as np  # numpy pour les maths , par exemple pour la racine carrée, il faut écrire np.sqrt
import matplotlib.pyplot as plt
from random import *
from tkinter import *


######################################################  CREATION D'UN TABLEAU AVEC TKINTER ################################
def tableur(abs,ord,nom_abs,nom_ord,unite_abs,unite_ord):
    root=Tk()
    root.title('Tableur')


    b=Button(root, text=str(nom_abs)+'('+str(unite_abs)+')', width=10)
    b.grid(row=0,column=1,sticky=NSEW)


    b=Button(root, text=str(nom_ord)+'('+str(unite_ord)+')', width=10)
    b.grid(row=0,column=2,sticky=NSEW)


    for m in range(len(abs)):
        b=Button(root, text=str(m+1), width=10)
        b.grid(row=m+1,column=0,sticky=NSEW)



    cols_abs=[]
    for i in range (len (abs)):
        e = Entry(root, justify=CENTER)
        e.grid(row=i+1, column=1, sticky=NSEW)
        e.insert(END, '%.2e'%abs[i])
        cols_abs.append(e)

    cols_ord=[]
    for i in range (len (abs)):
        e = Entry(root, justify=CENTER)
        e.grid(row=i+1, column=2, sticky=NSEW)
        e.insert(END, '%.2e'%ord[i])
        cols_ord.append(e)


    root.mainloop()
###################################################   METHODE DES MOINDRES CARRES  ###################################################    
    
def moyenne (X): # fonction pour calculer la moyenne (renvoie la moyenne pour une liste)
    m = 0
    for x in X :
        m = m + x
    return m/ len(X)

def moyenne_quad (X): # fonction pour calculer la moyenne quadratique (renvoie la moyenne pour une liste)
    m = 0
    for x in X :
        m = m + x**2
    return m/ len(X)

def ecart_type (X): # fonction pour calculer l'ecart type (renvoie l'ecart type pour une liste)
    m = moyenne (X)
    u = 0
    for x in X :
        u = u + (x-m)**2
    return np.sqrt (u/len (X))
    



def cov (X,Y): # fonction pour calculer la covariance (renvoie la covariance pour deux listes)
    mx = moyenne (X)
    my = moyenne (Y)
    c= 0
    for i in range ( len (X)):
        c = c + (X[i]-mx)*(Y[i]-my)
    return c/ len(X)

def regrelin (X,Y): # fonction pour calculer les paramètres d'une régression linéaire, renvoie dans l'ordre pour deux listes (abscisse et ordonnée) : pente, ordonnée à l'origine et coefficient de corrélation
    pente = cov(X,Y)/ ecart_type (X)**2
    ordonnee = moyenne (Y)-pente * moyenne (X)
    coeff = cov(X,Y)/( ecart_type (X)* ecart_type (Y))
    coeff2= coeff**2
    return pente , ordonnee , coeff2

#######################################            ELIMINATION DE POINTS ABERRANTS            ###########################################
# fonction pour calculer de l'ecart type expérimental d'une liste (Eric)
def ecart_type_exp(V):
    v=0
    moy=moyenne(V)
    for i in range(len(V)):
        v+=(V[i]-moy)**2
    variance=v/(len(V)-1)
    ecart_type=np.sqrt(variance)
    return ecart_type
        
# fonction pour calculer les ordonnées de la droite des moindres carrés
def droite(a,o):
    ordon_reg=[]
    eq=regrelin(a,o)
    for i in range (len(a)):
        ordon_reg.append(eq[1]+eq[0]*a[i])
    return (ordon_reg)
    
# fonction pour calculer la liste des carrés des écarts à la droite
def carres_ecarts(a,o):
    L=[]
    U=droite(a,o)
    for i in range (len(a)):
        L.append((U[i]-o[i])**2)
    return (L)

# fonction qui calcule borne inf et borne max pour éliminer des éléments d'une liste, trop éloignés de la moyenne de la liste
def bornes(L):
    moye=moyenne(L)
    e_t=ecart_type_exp(L)
    mini=float(moye)-2*float(e_t)
    maxi=float(moye)+2*float(e_t)
    return mini,maxi

# fonction qui conserve l'élément a[i] dans X et l'élément o[i] dans Y si mini < L[i] < maxi
def troncature(a,o,L,mini,maxi):
    X,Y=[],[]
    for i in range (len(L)):
        if L[i]<=maxi and L[i]>=mini:
            X.append(a[i])
            Y.append(o[i])
    return (X,Y)

# fonction pour eliminer des points aberrants
def elimination_valeurs(a,o):
    i=0
    X,Y=[],[]
    X=a
    Y=o
    while True:
        L=carres_ecarts(X,Y)
        mini,maxi=bornes(L)
        X,Y=troncature(a,o,L,mini,maxi)
        i+=1
        if len(L)== len(X):
            if i!=1:
                print('Nombre de points éliminés : ',i-1)
            else :
                print('Pas de points éliminés !')
            False
            return (X,Y)
            
            
################################################   CALCUL DES INCERTITUDES  #######################################################

def sigma_y (X,Y):# ecart données expérimentales/modèle
    a,b,r= regrelin (X,Y)
    Yth = [(a*elt+b) for elt in X]
    sigmay=0
    for i in range (len (X)):
        sigmay+=(Yth[i]-Y[i])**2
    sigmay = np.sqrt(sigmay/(len (Yth)-2))
    return sigmay

def sigma_a (X,Y): # incertitude sur pente
    a,b,r= regrelin (X,Y)
    Yth = [(a*elt+b) for elt in X]
    return  sigma_y(X,Y)/ecart_type(X)

def sigma_b (X,Y) : # incertitude sur origine à l'ordonnée
    return  sigma_a(X,Y)*np.sqrt(moyenne_quad (X))

def pourcent (X,Y): # ecart relatif données expérimentales/modèle en %
    a,b,r2 = regrelin (X,Y)
    Yth = [(a*elt+b) for elt in X]
    pourcent = 0
    count = 0
    for i in range (len(Yth)):
        if Yth[i]!=0 and ((Yth[i]-Y[i])/Yth[i])!=1:
            # pourcent+=((Yth[i]-Y[i])/Yth[i])**2
            pourcent+=abs((Yth[i]-Y[i])/Yth[i])
            count +=1
    # pourcent = 100* (np.sqrt(pourcent))/count
    pourcent = 100* pourcent/count
    return pourcent

#########################################################   RECUPERATION DE L'EQUATION DU MODELE RECUPERE  ############################################
def valeurs_calc (Xcalc,X,Y): # 
    Xcalc = np.linspace(0,X[len(X)-1] , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de X
    a,b,r2 = regrelin (X,Y)
    Ycalc = [(a*elt+b) for elt in Xcalc]
    return Ycalc
    


def reglin (X,Y,nomX,nomY): # pour afficher l'équation en chaîne de caractères, indiquer les abscisses, ordonnées en précisant les noms avec 'nom' et digits
    a,b,r2= regrelin (X,Y)
    equation = nomY+' = '+str('%.2e'%a)+' '+nomX+' + '+str('%.2e'%b)+'        r² ='+str('%.5e'%r2)
    equation = str(equation)
    equation2 = equation.replace('+ (-','- (') # pour une présentation plus élégante quand le nombre est négatif
    equation3=equation2.replace('e+00','') # ne pas afficher le 10 puissance 0
    print (equation3)
    print ('a ='+str('%.2e'%a)+'      ± ('+str('%.2e'%sigma_a(X,Y))+')')
    print ('b ='+str('%.2e'%b)+'      ± ('+str('%.2e'%sigma_b(X,Y))+')')
    print ('Ecart données modèle : ','%.2e'%sigma_y(X,Y))
    print ('Ecart données modèle en % : ',round(pourcent(X,Y),2),'%')
    return equation3
    
def reglin_avec_elimination (X,Y,nomX,nomY): # pour afficher l'équation en chaîne de caractères, indiquer les abscisses, ordonnées en précisant les noms avec 'nom' et digits
    X1,Y1 = elimination_valeurs(X,Y) #on élimine les points trop éloignés du modèle
    elimineX=[i for i in X if i not in X1]
    elimineY=[i for i in Y if i not in Y1]
    a,b,r2= regrelin (X1,Y1)
    equation = nomY+' = '+str('%.2e'%a)+' '+nomX+' + '+str('%.2e'%b)+'        r² ='+str('%.2e'%r2)
    equation = str(equation)
    equation2 = equation.replace('+ (-','- (') # pour une présentation plus élégante quand le nombre est négatif
    equation3=equation2.replace('e+00','') # ne pas afficher le 10 puissance 0
    print (equation3)
    
    print ('a ='+str('%.2e'%a)+'      ± ('+str('%.2e'%sigma_a(X1,Y1))+')')
    print ('b ='+str('%.2e'%b)+'      ± ('+str('%.2e'%sigma_b(X1,Y1))+')')
    print ('Ecart données modèle : ','%.2e'%sigma_y(X1,Y1))
    print ('Ecart données modèle en % : ',round(pourcent(X1,Y1),2),'%')
    if len(X)!= len(X1):
        print ('Valeurs éliminées de '+nomX+': ',elimineX)
        print ('Valeurs éliminées de '+nomY+': ',elimineY)

    return equation3

###############################################################################################################################

def saisie() :

    valeurs_x=[]
    valeurs_y=[]
    nom_x = str(input('Nom abscisse : '))
    unites_x = str(input('Unité abscisse : '))
    nom_y = str(input('Nom ordonnée : '))
    unites_y = str(input('Unité ordonnée : '))
    continuer=True
    print ('A la fin de la saisie appuyer sur Q')
    print ('Pour recommencer la saisie de valeurs appuyer sur R')
    while continuer:
        x=input(nom_x+': ')
        if x == 'r' or x == 'R':
            valeurs_x =[]
            valeurs_y=[]
            print ('Recommencez !')
            continue
            
        else:    
            if x!= 'q' :
                try :
                    x =float(x)
                except ValueError:
                    print('Erreur de saisie')
                    continue
                valeurs_x.append(x)
            else:
                print ('Fin de la saisie')
                continuer=False
                break
    
        y=input(nom_y+': ')
        if y == 'r' or y == 'R':
            valeurs_x =[]
            valeurs_y =[]
            print ('Recommencez !')
            continue
        else:
            if y!='q':
                try :
                    y =float(y)
                except ValueError:
                    valeurs_x.remove(x)
                    print('Erreur de saisie')
                    continue
                valeurs_y.append(y)
            else:
                valeurs_x.remove(x)
                print ('Fin de la saisie')
                continuer=False
                break
    
    
    return valeurs_x, valeurs_y,nom_x,nom_y,unites_x,unites_y


########################################  CETTE FONCTION PERMET DE FAIRE UNE REGRESSION LINEAIRE A PARTIR D'UNE SAISIE DE POINTS ####################        
def regclavier_avec_elimination (): # Affichage des courbes et équations avec saisie clavier en précisant  nombre de décimales
    continuer = True
    liste_marqueurs = ['+','o','*','v', '<']
    liste_couleurs = ['b', 'g', 'r', 'c', 'm',]
    i=0
    while continuer :
        X,Y,nomX,nomY,unitesx,unitesy = saisie()
        
        equation = reglin_avec_elimination (X,Y,nomX,nomY)
        M=np.array([X,Y])    
        M1 =np.transpose(M)
        print (M1)
        np.savetxt('donnees.txt'+str(i),M1) 
        Xcalc = np.linspace(0,X[len(X)-1] , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
        Ycalc = valeurs_calc(Xcalc,X,Y) # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
        
        suite = input ('Voulez-vous ajouter une courbe ? O/N : ')     
        i+=1
        if i>4:
            i=0
        if suite == 'n' or suite =='N':
            continuer = False
        color = liste_couleurs[i]
        marqueur = liste_marqueurs[i]
        
        plt.scatter(X,Y, c =str(color), marker = str(marqueur))
        plt.plot(Xcalc,Ycalc,color = str(color),label = equation)
    plt.title(nomY+' = '+'f('+nomX+')')
    plt.xlabel(nomX+' en '+unitesx)       #nommer l'axe des abscisses#
    plt.ylabel(nomY+' en '+unitesy)       #nommer l'axe des ordonnéees#
    plt.legend()   # pour afficher les légendes (label)
    plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
        
        
    tableur (X,Y,nomX,nomY,unitesx,unitesy)



                  
    return equation

def regclavier (): # Affichage des courbes et équations avec saisie clavier en précisant  nombre de décimales
    continuer = True
    liste_marqueurs = ['+','o','*','v', '<']
    liste_couleurs = ['b', 'g', 'r', 'c', 'm',]
    i=0
    while continuer :
        X,Y,nomX,nomY,unitesx,unitesy = saisie()
        
        equation = reglin (X,Y,nomX,nomY)
    
        M=np.array([X,Y])    
        M1 =np.transpose(M)
        print (M1)
        np.savetxt('donnees.txt'+str(i),M1) 
        Xcalc = np.linspace(0,X[len(X)-1] , 256) # création de points pour le tracé du modèle : on crée 256 points régulièrement espacés entre 0 et la valeur max de I
        Ycalc = valeurs_calc(Xcalc,X,Y) # on fait calculer U avec les paramètres de la régression linéaire pour ces valeurs de I
       
        
        suite = input ('Voulez-vous ajouter une courbe ? O/N : ')     
        i+=1
        if i>4:
            i=0
        if suite == 'n' or suite =='N':
            continuer = False
            
        color = liste_couleurs[i]
        marqueur = liste_marqueurs[i]    
       
        plt.scatter(X,Y, c =str(color), marker = str(marqueur))
        plt.plot(Xcalc,Ycalc,color = str(color),label = equation)
    plt.title(nomY+' = '+'f('+nomX+')')
    plt.xlabel(nomX+' en '+unitesx)       #nommer l'axe des abscisses#
    plt.ylabel(nomY+' en '+unitesy)       #nommer l'axe des ordonnéees#
    plt.legend()   # pour afficher les légendes (label)
    plt.show()  #afficher le graphique (ne rien mettre dans la parenthèse)
    
        
    tableur (X,Y,nomX,nomY,unitesx,unitesy)



                  
    return equation

    


 


# test des fonctions
if __name__ == "__main__":
    
    # regclavier()
  
    regclavier_avec_elimination()
    