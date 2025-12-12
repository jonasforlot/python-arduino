import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button
import time

# --- données ---
liste_temps_mesure = []
liste_temps = []
liste_conductiv = []

t_acquisition = 30.0
conductivmax = 500
conductivmin = 0
stop_acquisition = False

# --- récupération port USB ---
def recup_port_USB():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'USB' in p.description:
            return serial.Serial(p.device, 9600)
    return None

Data = recup_port_USB()
t0 = time.time()  # référence pour le temps

# --- figure ---
fig = plt.figure(figsize=(7,5))
line, = plt.plot([], [])
plt.xlim(0, t_acquisition)
plt.ylim(conductivmin, conductivmax)
plt.xlabel('temps en s')
plt.ylabel('conductiv en mS/m')
plt.grid()

# --- bouton STOP ---
ax_button = plt.axes([0.8, 0.02, 0.15, 0.07])
button = Button(ax_button, "STOP", color="lightcoral", hovercolor="red")

def stop(event):
    global stop_acquisition
    stop_acquisition = True
    print("Acquisition stoppée par l'utilisateur")
    plt.close(fig)  # ok ici car figure visible et callback séparé

button.on_clicked(stop)

# --- animation ---
def animate(i):
    global stop_acquisition

    # arrêt automatique après t_acquisition
    t_reel = time.time() - t0
    if t_reel >= t_acquisition:
        stop_acquisition = True
        return line,  # <-- ne PAS fermer la figure ici

    # lecture série (non bloquante)
    if Data.in_waiting > 0:
        line1 = Data.readline()
        donnees = line1.strip().split()
        if len(donnees) == 5:
            try:
                conductiv = float(donnees[2][:-4].decode())
            except:
                return line,
            liste_temps_mesure.append(time.time())
            liste_temps.append(t_reel)
            liste_conductiv.append(conductiv)
            print("Conductivité = %f mS/m, temps = %.2f s" % (conductiv, t_reel))
            line.set_data(liste_temps, liste_conductiv)
    return line,

ani = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False)

plt.show()  # <-- figure reste ouverte jusqu'à ce que stop_acquisition True ou bouton STOP

Data.close()

# --- fin d'acquisition ---
print("Fin de l'acquisition après %.1f s" % t_acquisition)

# --- figure finale ---
plt.figure()
plt.title('Conductivité=f(t)')
plt.scatter(liste_temps, liste_conductiv, color='r', marker='o')
plt.xlabel('temps en s')
plt.ylabel('conductivité en mS/m')
plt.show()

# --- sauvegarde ---
lines = ['t\tm\n']
for i in range(len(liste_conductiv)):
    lines.append(f"{liste_temps[i]}\t{liste_conductiv[i]}\n")
open('U:\\Documents\\data_arduino.txt', 'w').writelines(lines)
