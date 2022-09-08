import serial
import serial.tools.list_ports   # pour la communication avec le port série



#initialisation des listes
liste_masse = []


# Fonction pour la récupération des données série venant du port USB
def recup_port_usb() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) #Print and check if the port is open
    print(mData.name) # Print the name of the port
    return mData

Data =recup_port_usb()

# Essai pour une succession de 20 lignes de données
for k in range(20) :
    line1 = Data.readline() 
    print (line1)
    donnee=line1.strip().split()

    if len(donnee) !=0 :
        masse = float(donnee[1].decode())  # après consulation des données, nous choisissons le 2ème élément de listeDonnees
        liste_masse.append(masse)
        print ("masse : ", masse, " g")
Data.close()



#Ecriture dans un fichier txt
lines=['t\tm\n'] #première ligne du fichier txt
for i in range (len (liste_masse)):
    line = str(liste_temps[i]) +'\t'+ str(liste_masse[i])+'\n'
    lines.append(line)

fichier = open('data_balance.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte
