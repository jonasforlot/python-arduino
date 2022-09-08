#importation des modules
import serial
import serial.tools.list_ports # pour la communication avec le port série
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation # pour la figure animée
# import time # gestion du temps
import numpy as np # numpy pour l'importation des donnees en format txt
from scipy.optimize import curve_fit

liste_a1 = [] # liste pour stocker les valeurs d'acceleration
liste_a2 = [] # liste pour stocker les valeurs d'acceleration
liste_t = []
t_acquisition = 5.0 # en s
amax = 2.2 # en g
amin= -2.2 # en g

# dt=0.1


#pour le graphe en temps réel
def animate(i):
    global sys,line0,line1,t0,t1,u0,u1
    line_data = Data.readline()
    print (line_data)
    # on retire les caractères d'espacement en début et fin de chaîne
    listeDonnees = line_data.strip()
    # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
    listeDonnees = line_data.split()
    print (listeDonnees)


    if len(listeDonnees) == 6 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
        accel1 = (float(listeDonnees[2].decode()))/16834 # après consulation des données, nous choisissons le 2 ème élément de listeDonnees, on convertit l'accélération en g
        accel2 = (float(listeDonnees[5].decode()))/16834 # après consulation des données, nous choisissons le 3 ème élément de listeDonnees, on convertit l'accélération en g

        temps = (float(listeDonnees[0].decode()))/1000.0 # après consulation des données, nous choisissons le 1er élément de listeDonnees

        while temps <= t_acquisition:
            liste_a1.append(accel1)
            print("a1 = %f"%(accel1), " g") # affichage de la valeur de l'acceleration
            liste_a2.append(accel2)
            print("a2 = %f"%(accel2), " g") # affichage de la valeur de l'accelerat
            liste_t.append(temps)
            print("temps = %f"%(temps), " s") # affichage de la valeur du temps en partant de 0
            line0.set_data(liste_t,liste_a1)
            line1.set_data(liste_t,liste_a2)
            return line0,line1,






# Fonction pour la récupération des données série venant de la carte Arduino
def recup_port_Arduino() :
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description :
            mData = serial.Serial(p.device,9600)
    print(mData.is_open) # Affiche et vérifie que le port est ouvert
    print(mData.name) # Affiche le nom du port
    return mData






Data =recup_port_Arduino() #récupération des données




# Création figure
fig,(ax1,ax2) = plt.subplots(2,figsize=(10,10))
line0, = ax1.plot([],[],'r-')
line1, = ax2.plot([],[])
ax1.set_xlabel('temps en s')
ax1.set_ylabel('a1 en m/s²')
ax1.axis([0,t_acquisition,-2.2,amax])
ax2.set_xlabel('temps en s')
ax2.set_ylabel('a2 en m/s²')
ax2.axis([0,t_acquisition,-2.2,amax])



#Animation
ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)

plt.show()

plt.close(fig)
Data.close()




#Ecriture dans un fichier txt
lines=['t\ta\n'] #première ligne du fichier txt
for i in range (len (liste_a1)):
    line = str(liste_t[i]) +'\t'+ str(liste_a1[i])+'\n'
    lines.append(line)

fichier = open('data_accelerometre.txt', 'w')
fichier.writelines(lines) #création d'un nouveau fichier texte



# t = np.array(liste_t)
# accx = np.array(liste_ax)
# accy = np.array(liste_ay)
# accz = np.array(liste_az)
#
# def estim_freq(y) :
#     compt = 0
#     moy = np.mean(y)
#     etat_old = False
#     etat_new = False
#     for i in range (len(y)) :
#         if  y[i] < moy :
#             etat_new = True
#         else :
#             etat_new = False
#         if etat_old != etat_new :
#             etat_old = etat_new
#             compt += 1
#
#     return (compt/(2*t_acquisition))
#
#
# def get_p0(x, y):
#
#     A0 = (np.max(y)-np.min(y))/2
#     f0 =estim_freq(y)
#     phase0 =0
#     offset0 = np.mean(y)
#
#
#     return [A0, f0, phase0,offset0]
#
# def f(x,a,b,c,d):
#     return (a*np.sin(2.*np.pi*b*x+c)+d)
#
# Xcalc = np.linspace(0,max(t) , 2048) # création de points pour le tracé du modèle : on crée 1024 points régulièrement espacés entre 0 et la valeur max de I
#
#
# popt,pcov = curve_fit (f,t,accx,p0=get_p0(t,accx))
#
# # pop,pcov = curve_fit (f,t,acc)
#
# texte = 'Accélération = '+str(round(float(popt[0]),2))+' sin (2pi*'+str(round(float(popt[1]),2))+'*t+'+str(round(float(popt[2]),2))+') + '+str(round(float(popt[3]),2))+'\n' +'A = '+str(round(float(popt[0]),2))+'; f = '+str(round(float(popt[1]),2))+' ; phase ='+str(round(float(popt[2]),2))+' ; offset = '+str(round(float(popt[3]),2))
#
#
# # Création figure
# fig,(ax1,ax2,ax3) = plt.subplots(3,figsize=(10,10))
# ax1.scatter(t, accx, c = 'red', marker = '+')
# ax1.plot(Xcalc,f(Xcalc,*popt),'g--',label = texte)
# ax1.set_xlabel('temps en s')
# ax1.set_ylabel('ax en m/s²')
# ax1.axis([0,t_acquisition,0,amax])
# plt.scatter(t, accy, c = 'blue', marker = '*')
# ax2.set_xlabel('temps en s')
# ax2.set_ylabel('ay en m/s²')
# ax2.axis([0,t_acquisition,0.0,amax])
# plt.scatter(t, accz, c = 'green', marker = '.')
# ax3.set_xlabel('temps en s')
# ax3.set_ylabel('az en m/s²')
# ax3.axis([0,t_acquisition,0.0,amax])
# print (texte)

