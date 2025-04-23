import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib import animation
import time
import sys

# Paramètres d'acquisition
T_ACQUISITION = 10.0  # durée en secondes


MMAX = 90
MMIN = -90

# Listes de stockage
liste_temps = []
liste_angle = []

# Préparation du graphe
fig = plt.figure()
(line,) = plt.plot([], [])
plt.xlim(0, T_ACQUISITION)
plt.ylim(MMIN, MMAX)
plt.xlabel("temps (s)")
plt.ylabel("angle (°)")
plt.grid()

# Fonction génératrice : lecture depuis Arduino
def angle_depuis_arduino():
    ports = list(serial.tools.list_ports.comports())

    arduino_data = None
    for p in ports:
        if "Arduino" in p.description:
            arduino_data = serial.Serial(p.device, 9600)

    if not arduino_data:
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

            yield temps, angle
        except Exception as e:
            print(f"Erreur de lecture : {e}")
            break

    print("Fermeture du port du Arduino")
    arduino_data.close()


# Fonction pour l'animation matplotlib
def animate(data):
    temps, angle = data

    if temps >= T_ACQUISITION:
        print("Temps max atteint – arrêt de l'animation.")
        ani.event_source.stop()
        return

    liste_temps.append(temps)
    liste_angle.append(angle)
    print(f"angle = {angle:+.2f}° | temps = {temps:.3f}s")

    line.set_data(liste_temps, liste_angle)
    return (line,)

# Lancement de l'animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=angle_depuis_arduino,
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
