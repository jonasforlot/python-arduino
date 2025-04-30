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
T_ACQUISITION = 10.0  # durée en secondes


vmin = 0
vmax = 15

# Listes de stockage
liste_temps = []
liste_vitesse = []

# Préparation du graphe
fig = plt.figure()
(line,) = plt.plot([], [])
plt.xlim(0, T_ACQUISITION)
plt.ylim(vmin, vmax)
plt.xlabel("temps (s)")
plt.ylabel("vitesse (m/s")
plt.grid()

# TIPS: penser à changer le nom de son générateur quand il retourne plus la même chose '^_^
# Fonction génératrice : lecture depuis Arduino
def temps_vitesse_depuis_arduino():
    arduino_data = None
    for com_port in serial.tools.list_ports.comports():
        if "Arduino" in com_port.description:
            arduino_data = serial.Serial(com_port.device, 9600)

    print(f"Le port arduino utilisé : {arduino_data.name}")
    print(f"Est-il ouvert ? {arduino_data.is_open}")


    while True:
        try:
            line = arduino_data.readline()
            liste_donnees = line.split()

            vitesse = float(liste_donnees[1].decode())
            temps = float(liste_donnees[0].decode()) / 1000.0

            # TIPS: Il suffit de tester le temps ici pour sortir de la boucle
            if temps >= T_ACQUISITION:
                print("Temps max atteint – arrêt de l'animation.")
                break

            yield temps, vitesse
        except Exception as e:
            print(f"Erreur de lecture : {e}")
            break

    print("Fermeture du port du Arduino")
    arduino_data.close()


# Fonction pour l'animation matplotlib
def animate(data):
    temps, vitesse = data

    liste_temps.append(temps)
    liste_vitesse.append(vitesse)


    print(f"vitesse = {vitesse:+6.2f}m/s | temps = {temps:6.3f}s")

    line.set_data(liste_temps, liste_vitesse)
    return (line,)

# Lancement de l'animation
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=temps_vitesse_depuis_arduino,
    interval=0,
    repeat=False,
    cache_frame_data=False
)

plt.show()
plt.close(fig)

# Sauvegarde des données dans un fichier texte
with open("data_arduino.txt", "w") as fichier:
    fichier.write("temps_s\tvitesse_deg\n")
    for t, a in zip(liste_temps, liste_vitesse):
        fichier.write(f"{t:.3f}\t{a:.2f}\n")

print("Les données ont été enregistrées dans 'data_arduino.txt'.")
