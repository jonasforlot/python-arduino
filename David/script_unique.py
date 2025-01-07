import sys
import os
import serial
import serial.tools.list_ports
import matplotlib
matplotlib.use('TkAgg')  # Forcer l'utilisation du backend TkAgg pour matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import os
import tkinter as tk
from tkinter import simpledialog

# Variables globales pour t_acquisition et emax
t_acquisition = 60.0  # Valeur par défaut
e_max = 4000  # Valeur par défaut

# Détecter si l'application est exécutée en tant que fichier .exe
if getattr(sys, 'frozen', False):
    # Si exécuté en tant qu'exécutable, obtenir le chemin temporaire
    base_path = sys._MEIPASS
else:
    # Si exécuté en tant que script Python, obtenir le répertoire du script
    base_path = os.path.dirname(__file__)

# Construire le chemin complet de l'icône
icon_path = os.path.join(base_path, 'icone.ico')


def recup_port_Arduino():
    """Récupérer le port Arduino"""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description or 'CDC' in p.description or 'USB' in p.description:
            mData = serial.Serial(p.device, 9600)
            print(mData.is_open)
            print(mData.name)
            return mData
    raise Exception("Aucun appareil Arduino trouvé sur les ports séries")

def acquisition():
    global t_acquisition, e_max

    liste_e = []  # Liste pour stocker les valeurs d'éclairement
    liste_t_mesure =[] # liste pour stocker le temps"brut"
    liste_t = []
    emin = 0  # en lux

    # Fonction pour le graphe en temps réel
    def animate(i):
        line1 = Data.readline()
        print(line1)
        listeDonnees = line1.strip().split()
        print(listeDonnees)

        if len(listeDonnees) == 2:
            eclairement = float(listeDonnees[1].decode())
            temps = float(listeDonnees[0].decode()) / 1000.0
            liste_t_mesure.append(temps)
            if liste_t_mesure[0]< 1 : # pour éventuellement éliminer les premières valeurs fausses de temps (défaut d'Arduino)

                while temps <= t_acquisition:
                    liste_e.append(eclairement)
                    print("Eclairement = %f" % (eclairement), " lux")
                    liste_t.append(temps)
                    line.set_data(liste_t, liste_e)
                    return line,

            else :
                del liste_t_mesure[0]

    Data = recup_port_Arduino()

    # Création de la figure
    fig = plt.figure()
    line, = plt.plot([], [])
    plt.xlim(0, t_acquisition)
    plt.ylim(emin, e_max)
    plt.xlabel('temps en s')
    plt.ylabel('éclairement en lux')
    plt.grid()

    # Animation
    ani = animation.FuncAnimation(fig, animate, frames=2000, interval=20, repeat=False)
    plt.show()  # Afficher la figure animée

    Data.close()

    # Sauvegarde des données dans un fichier texte
    nom_fichier_base = "eclairement"
    compteur = 0
    while os.path.exists(f"{nom_fichier_base}{compteur}.txt"):
        compteur += 1

    nom_fichier = f"{nom_fichier_base}{compteur}.txt"
    lines = ['t\ta\n']
    for i in range(len(liste_e)):
        line = f"{liste_t[i]}\t{liste_e[i]}\n"
        lines.append(line)

    with open(nom_fichier, 'w') as fichier:
        fichier.writelines(lines)

    print(f"Fichier créé : {nom_fichier}")

    # Affichage des points
    t = np.array(liste_t)
    ecl = np.array(liste_e)

    plt.figure()
    plt.scatter(t, ecl, c='red', marker='+')
    plt.plot(t, ecl, label='Eclairement en fonction du temps')
    plt.xlabel("Temps en s")
    plt.ylabel("Eclairement en lux")
    plt.legend()
    plt.show()

def interface(root):
    global t_acquisition, e_max

    def definir_parametres():
        """Demander les paramètres t_acquisition et emax"""
        global t_acquisition, e_max
        t_acquisition = simpledialog.askfloat("Temps d'acquisition", "Entrez le temps d'acquisition (en secondes) :", initialvalue=t_acquisition)
        e_max = simpledialog.askfloat("Eclairement maximum", "Entrez la valeur maximum d'éclairement (en lux) :", initialvalue=e_max)
        tk.Label(root, text=f"Temps d'acquisition : {t_acquisition}s\nEclairement max : {e_max} lux", font=("Arial", 10)).pack(pady=10)

    # Bouton pour définir les paramètres
    bouton_parametres = tk.Button(root, text="Définir les paramètres", font=("Arial", 12), command=definir_parametres)
    bouton_parametres.pack(pady=10)

    # Bouton pour lancer l'acquisition
    bouton_acquisition = tk.Button(root, text="Lancer la mesure", font=("Arial", 12), fg="blue", command=lambda: [root.quit(), acquisition()])
    bouton_acquisition.pack(pady=20)

    # Lancer l'interface graphique
    root.mainloop()

if __name__ == "__main__":
    # Créer la fenêtre principale une seule fois
    root = tk.Tk()
    root.title("Interface de mesure")
    root.iconbitmap(icon_path)  # Charger l'icône depuis le chemin dynamique

    # Lancer l'interface
    interface(root)
