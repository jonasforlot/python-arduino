# importation des modules
import serial
import serial.tools.list_ports  # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation  # pour la figure animée
import time  # gestion du temps
import sys  # pour pouvoir sortir du programme en cas d'erreur
from math import sin  # pour faire de fausses données

# BUG: pas vraiment un bug mais c'est une norme --> les constantes comme ça pour tout le fichier s'écrive en majuscule pour les distinguer du reste
T_ACQUISITION = 10.0  # en sec
T_INTERVAL = 20  # en millisec
NB_FRAME = int((T_ACQUISITION * 1000) // T_INTERVAL)  # c'est une division entière
MMAX = 100  # en degré
MMIN = -100


# je te présente mon fake arduino !
#class FakeData:
#    def readline(self):
#        val1 = MMAX * sin(time.time())
#        val2 = 0.00234 * val1 - 0.328
#        return f"{val1}\t{val2}".encode("ascii")

#   def close(self):
#       pass


# initialisation des listes
liste_temps_mesure = []  # liste pour stocker le temps"brut"
liste_temps = []  # liste pour stocker les valeurs de temps en partant de t=0
liste_angle = []  # liste pour stocker les valeurs de concentration


# BUG: le nom de la fonction n'était pas adapté, car elle ne récupère pas le port arduino mais les données depuis ce port
# Fonction pour la récupération des données série venant de la carte Arduino
def recup_data_depuis_port_Arduino():
    ports = list(serial.tools.list_ports.comports())

    # BUG: j'ai ajouté une gestion d'erreur pour les couillons qui oublient de brancher le arduino
    mData = None
    for p in ports:
        if "Arduino" in p.description:
            mData = serial.Serial(p.device, 9600)

    if not mData:
        sys.exit(
            "Aucun port arduino trouvé, vérifiez si le arduino est bien branché à l'ordi"
        )

    print(mData.is_open)  # Affiche et vérifie que le port est ouvert
    print(mData.name)  # Affiche le nom du port
    return mData


# récupération des données
Data = recup_data_depuis_port_Arduino()
#Data = FakeData()

# Création figure
fig = plt.figure()
(line,) = plt.plot([], [])
plt.xlim(0, T_ACQUISITION)
plt.ylim(MMIN, MMAX)
plt.xlabel("temps en s")
plt.ylabel("angle en degré")
plt.grid()


# pour le graphe en temps réel
def animate(i):
    # BUG: pour permettre de bien comprendre les fonction et éviter des bug attroces il faut toujours signaler qu'on utilise une variable
    # BUG(suite): définie à l'extérieur de la fonction. Il y a un mot clé "global" pour ça en python qui évite que tu redéclare une variable sans le faire exprès
    # BUG(suite): certain le mettent au début de leur fonction d'autres juste avant d'utiliser la variable pour la première fois
    global liste_temps_mesure
    global liste_temps
    global liste_angle
    global line
    global Data

    line1 = Data.readline()
    # print(line1)
    # BUG: tu faisait strip() puis split() mais tu écrasais le résultat de de strip() par celui de split ça marchait car en fait split fait naturellement un strip avant d'agir
    # # on retire les caractères d'espacement en début et fin de chaîne
    # listeDonnees = line1.strip()
    # # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    # listeDonnees = line1.split()

    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line1.split()
    # print(listeDonnees)

    # BUG: il faqut éviter de fqire un if pour "éviter" ça rend le code plus complexe -> on préfère fqire un if qui sort explicitement pour le cas foireux
    # BUG(suite): et pour tester si une liste est vide on préfère tester directement la liste if not ma_liste:
    # # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
    # if len(listeDonnees) == 1:

    # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
    if not listeDonnees:
        # nous n'avons pas de donnée alors on retourne la ligne inchangée
        return (line,)

    # BUG: ici tu dis que tu prends le 2eme élément mais tu prends en fait le 1er
    # après consulation des données, nous choisissons le 2ème élément de listeDonnees
    angle = float(listeDonnees[1].decode())

    # temps mesuré "brut" stocké dans une liste
    # BUG: pas vraiment un bug mais autant être cohérent tempsmes -> temps_mes c'est comme ça que tu as écrit les autres variables
    temps_mes = time.time()
    liste_temps_mesure.append(temps_mes)

    # pour faire partir le temps de 0 (cette valeur de temps sera stockée dans une autre liste : liste_temps)
    tempsreel = temps_mes - liste_temps_mesure[0]

    # BUG: en fait ce while ne sert à rien car on ne chope pas le temps dedans et en plus on le quitte au premier tour
    # BUG(suite): c'est en fait pas ici qu'on doit fixer le temps de l'acquisition... mais à l'appel de
    # while tempsreel <= T_ACQUISITION:

    # LISIBILITÉ: j'ai regroupé les append pour plus de lisibilité
    liste_angle.append(angle)
    liste_temps.append(tempsreel)

    # BONNE PRATIQUE: on ne doit plus utiliser le % pour les chaines de caractère depuis... 10 ans, on utilise les f-string à la place
    # BONNE PRATIQUE: j'ai aligné les = pour plus de lisibilité et fixé la longueur de float affichés et tout mis sur une ligne pour avoir une mesure/ligne
    print(
        f"angle = {angle:+15.6f} degré | temps mesuré = {temps_mes:15.6f} s | temps réel = {tempsreel:15.6f} s"
    )

    # on fixe les point de la nouvelle frame
    line.set_data(liste_temps, liste_angle)

    return (line,)


# Animation
# BUG: en fait c'est ici que tu fixe le temps de la mesure... et tu avais mis 2000 frame de 20 millisec donc 40 seconde de mesure
# ani = animation.FuncAnimation(fig, animate, frames=2000, interval=20, repeat=False)
# Là je fixe pas 2000 frames... je calcule le nombre de frame nécessaire
ani = animation.FuncAnimation(
    fig, animate, frames=NB_FRAME, interval=T_INTERVAL, repeat=False
)


plt.show()


plt.close(fig)
Data.close()  # pour arrêter la lecture des données série


# # Ecriture dans un fichier txt
# lines = ["t\tm\n"]  # première ligne du fichier txt
# for i in range(len(liste_masse)):
#     line = str(liste_temps[i]) + "\t" + str(liste_masse[i]) + "\n"
#     lines.append(line)


# fichier = open("U:\Documents\\data_arduino.txt", "w")
# fichier.writelines(lines)  # création d'un nouveau fichier texte
