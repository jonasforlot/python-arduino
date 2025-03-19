#Importation des modules
import serial
import serial.tools.list_ports   # pour la communication avec le port série



#initialisation des listes
liste_temps=[] # liste pour stocker les valeurs de temps en s
liste_distance = [] # liste pour stocker la distance en mm

t_acquisition = 5.0


# Fonction pour la récupération des données série venant du port USB
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
        # if 'CDC' in p.description :    #pour les utilisateurs de mac
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData

Data =recup_port_Arduino()

# Acquition temporelle
temps=0
while temps <= t_acquisition:
    line1 = Data.readline()
    print (line1)
    #on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line1.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    print (listeDonnees)

    if len(listeDonnees)== 2: # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        temps = float(listeDonnees[0].decode())/1000.0 # après consultation des données, nous choisissons le 1er élément de listeDonnees, conversion en secondes
        distance = float(listeDonnees[1].decode()) # après consultation des données, nous choisissons le 2ème élément de listeDonnees
        liste_temps.append(temps)
        liste_distance.append(distance)
        print("temps = %f"%(temps), " s") # affichage de la valeur du temps en partant de 0
        print("d = %f"%(distance), " mm") # affichage de la valeur de la distance en mm


Data.close()

# Ecriture dans un fichier txt
lines = ['t\td\n']  # première ligne du fichier txt
for i in range(len(liste_temps)):
    line = str(liste_temps[i]) +'\t'+str(liste_distance[i]) + '\n'
    lines.append(line)

# Utilisation de 'with open' pour assurer la fermeture du fichier
with open('data_arduino.txt', 'w', encoding='utf-8') as fichier:
    fichier.writelines(lines)  # création d'un nouveau fichier texte

