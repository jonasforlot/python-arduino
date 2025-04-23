# importation des modules
import serial
import serial.tools.list_ports  # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation  # pour la figure animée
import time  # gestion du temps
import sys  # pour pouvoir sortir du programme en cas d'erreur

from math import sin  # pour faire de fausses données
from dataclasses import dataclass  # pour faire de fausses données

T_ACQUISITION = 10.0  # en sec
T_INTERVAL = 50  # en millisec
T_INI = time.time()  # en sec
NB_FRAME = int((T_ACQUISITION * 1000) // T_INTERVAL)  # c'est une division entière

MMAX = 90  # en degré
MMIN = -90


# je te présente mon fake arduino !
#@dataclass
#class FakeData:
#    name = "fake data"
#    is_open = True
#
#    def readline(self):
#        val1 = MMAX * sin(time.time())
#        val2 = 0.00234 * val1 - 0.328
#        return f"{val1}\t{val2}".encode("ascii")

#    def close(self):
#        pass


# Création des listes pour stocker nos données
liste_temps_mesure = []  # liste pour stocker le temps"brut"
liste_temps = []  # liste pour stocker les valeurs de temps en partant de t=0
liste_angle = []  # liste pour stocker les valeurs d angle

# Création de la figure pour dessiner
fig = plt.figure()
(line,) = plt.plot([], [])
plt.xlim(0, T_ACQUISITION)
plt.ylim(MMIN, MMAX)
plt.xlabel("temps en s")
plt.ylabel("angle en degré")
plt.grid()


# un générateur pour lire les données du arduino
# INFO: avec cette version ici on fait que du arduino
def angle_depuis_arduino():
    # on commence par trouver sur quel port le arduino est connecté
    ports = list(serial.tools.list_ports.comports())

    arduino_data = None
    for p in ports:
        if "Arduino" in p.description:
            arduino_data = serial.Serial(p.device, 9600)

    if not arduino_data:
         sys.exit(
             "Aucun port arduino trouvé, vérifiez si le arduino est bien branché à l'ordi"
        )
    #arduino_data = FakeData()

    print(f"Le port arduino utilisé : {arduino_data.name}")
    print(f"Est-il ouvert ? {arduino_data.is_open}")

    # on boucle pour exactement le nombre de frame qu'il faut pour l'acquisition
    for _ in range(NB_FRAME):
        # on récupère la ligne de donnée
        line = arduino_data.readline()

        # on la découpe
        liste_donnees = line.split()

        # on récupère la masse
        angle = float(liste_donnees[1].decode())

        # on retourne la masse
        print(angle)
        yield angle

    print("Fermeture du port du Arduino")
    arduino_data.close()


# pour le graphe en temps réel
# INFO: avec cette version ici on fait que de la physique
def animate(angle):
    global liste_temps_mesure
    global liste_temps
    global liste_angle
    global line

    # temps mesuré "brut" stocké dans une liste
    temps_mes = time.time()

    # LISIBILITÉ: j'ai regroupé les append pour plus de lisibilité
    liste_angle.append(angle)
    liste_temps_mesure.append(temps_mes)


    # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)
    # temps_reel = temps_mes - T_INI
    temps_reel = temps_mes - liste_temps_mesure[0]

    liste_temps.append(temps_reel)


    print(
        f"angle = {angle:+15.6f} degré | temps mesuré = {temps_mes:15.6f} s | temps réel = {temps_reel:15.6f} s"
    )

    # on fixe les point de la nouvelle frame
    line.set_data(liste_temps, liste_angle)

    return (line,)


# Animation
ani = animation.FuncAnimation(
    fig,  # la figure ou on va dessiner l'animation
    animate,  # fonction qui génère les frame successive du graph et écrit les données dans les listes
    frames=angle_depuis_arduino,  # generateur qui passera des données à la fonction à chaque frame
    interval=T_INTERVAL,  # temps entre 2 frames
    repeat=False,  # on ne boucle pas quand on a finit
    save_count=NB_FRAME,  # le nombre de frame qu'on veut
)


plt.show()
plt.close(fig)

# # Ecriture dans un fichier txt
# lines = ["t\tm\n"]  # première ligne du fichier txt
# for i in range(len(liste_masse)):
#     line = str(liste_temps[i]) + "\t" + str(liste_masse[i]) + "\n"
#     lines.append(line)

# fichier = open("U:\Documents\\data_arduino.txt", "w")
# fichier.writelines(lines)  # création d'un nouveau fichier texte
