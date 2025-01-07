import tkinter as tk
import subprocess  # Pour exécuter un script Python

# Fonction pour lancer un script Python
def lancer_script():
    # Remplacez le chemin du script par celui de votre propre script Python
    subprocess.run(["python", "tracé graph ok.py"])

# Créer la fenêtre principale
root = tk.Tk()
root.title("Lancer un script Python")

# Créer un bouton pour lancer le script
button = tk.Button(root, text="Lancer la mesure",font=("Arial", 12), fg="blue", command=lancer_script)
button.pack(pady=20)

# Lancer l'interface graphique
root.mainloop()
