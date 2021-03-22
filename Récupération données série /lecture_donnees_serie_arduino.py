#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
import sys

# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    if len(ports) != 0 :
        print (ports)
        for p in ports:
            if 'Arduino' in p.description :
                mData = serial.Serial(p.device,9600)
                print("la carte Arduino est connectée sur le port "+str(mData.name)) # Affiche et vérifie que le port est ouvert
                return mData
            else :
                print ("Pas de carte Arduino détectée")
    else :
        print ("Pas de port actif")

         

            
   

Data =recup_port_Arduino() #récupération des données


print ("Test de lecture pour 20 lignes de données")

compt = 0
try : 
    for i in range(10) :     
        line1 = Data.readline() 
         # on retire les caractères d'espacement en début et fin de chaîne
        listeDonnees = line1.strip()
        # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
        listeDonnees = line1.split()
        if len (listeDonnees) != 0 :
            print ("Ligne de donnnées reçue : ",line1)
            print ("Liste des données de la ligne : ",listeDonnees)
        else :
            print ("Ligne vide")
            compt += 1
            
    if compt != 0 :
        print (compt, " lignes sur ",10," sont vides")
            
except AttributeError :
    print ("Pas de données reçues")


try : 
    # line1 = Data.readline() # on laisse passer la première ligne qui peut être incomplète
    while True :
        line1 = Data.readline() 
         # on retire les caractères d'espacement en début et fin de chaîne
        listeDonnees = line1.strip()
        # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
        listeDonnees = line1.split()
        if len (listeDonnees) != 0 :
            print ("Ligne de donnnées reçue : ",line1)
            print ("Séparation des "+str(len(listeDonnees))+" données de la ligne reçue:")
            for k in range(len(listeDonnees)) :
                print("Indice ",k," : ",listeDonnees[k].decode())
            break
except AttributeError :
    print ("Pas de données reçues")


Data.close()







