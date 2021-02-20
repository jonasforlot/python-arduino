#Importation des modules
import serial
import serial.tools.list_ports   # pour la communication avec le port série



#initialisation des listes
liste_distance = []


# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port 
    return mData
Data = recup_port_Arduino()

line1 = Data.readline() 
print (line1)
donnee=line1.strip().split()
print (donnee)