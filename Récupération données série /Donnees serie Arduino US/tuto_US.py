#Importation des modules
import serial
import serial.tools.list_ports   # pour la communication avec le port série


#initialisation des listes
liste_distance = []

# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        # if 'Arduino' in p.description :
        if 'CDC' in p.description :    #pour les utilisateurs de mac
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port 
    return mData

Data =recup_port_Arduino()

# Essai pour une succession de 20 lignes de données
for k in range(20) :
    line1 = Data.readline() 
    print (line1)
    donnee=line1.strip().split()
    print (donnee)

    if len(donnee) !=0 :    # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        distance = float(donnee[4].decode())  # après consulation des données, nous choisissons le 5ème élément de listeDonnees
        liste_distance.append(distance)
        print ("distance : ", distance, " mm")
Data.close()

#Ecriture dans un fichier txt
lines=['d\n'] #première ligne du fichier txt
for i in range (len (liste_distance)):
    line = str(liste_distance[i])+'\n'
    lines.append(line)

fichier = open('data_arduino.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte

