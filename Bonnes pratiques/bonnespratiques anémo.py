import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib import animation
import time
import sys
# Import pour mon fake arduino
from dataclasses import dataclass
from math import sin

# Paramètres d'acquisition
FAKE_ARDUINO = True  # Change ça à False pour utiliser le vrai arduino
T_ACQUISITION = 10.0  # durée en secondes


MMAX = 8
MMIN = 0

# je te présente mon fake arduino !
@dataclass
class FakeData:
    name = "fake data"
    is_open = True
    t_zero = None  # in ms

    def readline(self):
        # Comme ça on a un temps initial comme si c'était celui du arduino: il est initialisé que la première fois
        if self.t_zero is None:
            self.t_zero = time.time() * 1000.0

        t = (time.time() * 1000.0) - self.t_zero  # in ms
        fake_val = MMAX * sin(t / 1000.0)

        return f"{t}\t{fake_val}".encode("ascii")

    def close(self):
        pass

# Listes de stockage
liste_temps = []
liste_angle = []

# Préparation du graphe
fig = plt.figure()
(line,) = plt.plot([], [])
plt.xlim(0, T_ACQUISITION)
plt.ylim(MMIN, MMAX)
plt.xlabel("temps (s)")
plt.ylabel("vitesse (m/s")
plt.grid()

# TIPS: penser à changer le nom de son générateur quand il retourne plus la même chose '^_^
# Fonction génératrice : lecture depuis Arduino
def temps_angle_depuis_arduino():
    arduino_data = None
    for com_port in serial.tools.list_ports.comports():
        if "Arduino" in com_port.description:
            arduino_data = serial.Serial(com_port.device, 9600)

    if not arduino_data:
        if FAKE_ARDUINO:
            # Si le mode fake est activé on bascule dessus
            arduino_data = FakeData()
        else:
            sys.exit("Aucun port arduino trouvé, vérifiez si le arduino est bien branché à l'ordi")

    print(f"Le port arduino utilisé : {arduino_data.name}")
    print(f"Est-il ouvert ? {arduino_data.is_open}")

    #  On ne fait plus une boucle pour NB_FRAME, mais on lit tant que l’Arduino ne dit pas stop
    while True:
        try:
            line = arduino_data.readline()
            liste_donnees = line.split()

            angle = float(liste_donnees[1].decode())
            temps = float(liste_donnees[0].decode()) / 1000.0

            # TIPS: Il suffit de tester le temps ici pour sortir de la boucle
            if temps >= T_ACQUISITION:
                print("Temps max atteint – arrêt de l'animation.")
                break

            yield temps, angle
        except Exception as e:
            print(f"Erreur de lecture : {e}")
            break

    print("Fermeture du port du Arduino")
    arduino_data.close()


# Fonction pour l'animation matplotlib
def animate(data):
    temps, angle = data

    liste_temps.append(temps)
    liste_angle.append(angle)

    # TIPS: j'ai ajouté une longueur minimum pour l'affichage des nombre pour que ça reste bien aligner
    print(f"angle = {angle:+6.2f}° | temps = {temps:6.3f}s")

    line.set_data(liste_temps, liste_angle)
    return (line,)

# Lancement de l'animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=temps_angle_depuis_arduino,
    interval=0,
    repeat=False,
    cache_frame_data=False
)

plt.show()
plt.close(fig)

# Sauvegarde des données dans un fichier texte
with open("data_arduino.txt", "w") as fichier:
    fichier.write("temps_s\tangle_deg\n")
    for t, a in zip(liste_temps, liste_angle):
        fichier.write(f"{t:.3f}\t{a:.2f}\n")

print("Les données ont été enregistrées dans 'data_arduino.txt'.")
