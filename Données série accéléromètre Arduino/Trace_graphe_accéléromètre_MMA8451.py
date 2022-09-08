#importation des modules
 import serial
 import serial.tools.list_ports # pour la communication avec le port série
 import matplotlib.pyplot as plt  # pour le tracé de graphe
 from matplotlib import animation # pour la figure animée
 # import time # gestion du temps
 import numpy as np # numpy pour l'importation des donnees en format txt
 from scipy.optimize import curve_fit


 liste_a = [] # liste pour stocker les valeurs d'accélération
 liste_t = []
 t_acquisition = 10.0 # en s
 amax =2 # en g
 amin= -2 # en g


 # dt=0.1




 #pour le graphe en temps réel
 def animate(i):
     line1 = Data.readline()


     print (line1)
     # on retire les caractères d'espacement en début et fin de chaîne
     listeDonnees = line1.strip()
     # on sépare les informations reçues séparées par les espaces et on stocke ces informations dans une liste pour chacune de lignes
     listeDonnees = line1.split()
     print (listeDonnees)




     if len(listeDonnees) == 12 : # parfois des lignes de données vides peuvent être envoyées, il faut les "écarter"
         accel = (float(listeDonnees[5].decode()))/4096 # après consulation des données, nous choisissons le 6 ème élément de listeDonnees, on convertit l'accélération en g


         temps = (float(listeDonnees[2].decode()))/1000.0 # après consulation des données, nous choisissons le 1er élément de listeDonnees


         while temps <= t_acquisition:
             liste_a.append(accel)
             print("a = %f"%(accel), " g") # affichage de la valeur de l'accélération
             liste_t.append(temps)
             print("temps = %f"%(temps), " s") # affichage de la valeur du temps en partant de 0
             line.set_data(liste_t,liste_a)
             return line,












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
 fig=plt.figure()
 line, = plt.plot([],[])
 plt.xlim(0, t_acquisition)
 plt.ylim(amin,amax)
 plt.xlabel('temps en s')
 plt.ylabel('a en g')
 plt.grid()




 #Animation
 ani = animation.FuncAnimation(fig, animate, frames=2000,  interval=20,repeat=False)


 plt.show()


 plt.close(fig)
 Data.close()








 #Ecriture dans un fichier txt
 lines=['t\ta\n'] #première ligne du fichier txt
 for i in range (len (liste_a)):
     line = str(liste_t[i]) +'\t'+ str(liste_a[i])+'\n'
     lines.append(line)


 fichier = open('data_accelerometre.txt', 'w')
 fichier.writelines(lines) #création d'un nouveau fichier texte






 t = np.array(liste_t)
 acc = np.array(liste_a)




 def estim_freq(y) :
     compt = 0
     moy = np.mean(y)
     etat_old = False
     etat_new = False
     for i in range (len(y)) :
         if  y[i] < moy :
             etat_new = True
         else :
             etat_new = False
         if etat_old != etat_new :
             etat_old = etat_new
             compt += 1


     return (compt/(2*t_acquisition))




 def get_p0(x, y):


     A0 = (np.max(y)-np.min(y))/2
     f0 =estim_freq(y)
     phase0 =0
     offset0 = np.mean(y)




     return [A0, f0, phase0,offset0]


 def f(x,a,b,c,d):
     return (a*np.sin(2.*np.pi*b*x+c)+d)


 Xcalc = np.linspace(0,max(t) , 1024) # création de points pour le tracé du modèle : on crée 1024 points régulièrement espacés entre 0 et la valeur max de I




 popt,pcov = curve_fit (f,t,acc,p0=get_p0(t,acc))


 # pop,pcov = curve_fit (f,t,acc)


 texte = 'Accélération = '+str(round(float(popt[0]),2))+' sin (2pi*'+str(round(float(popt[1]),2))+'*t+'+str(round(float(popt[2]),2))+') + '+str(round(float(popt[3]),2))+'\n' +'A = '+str(round(float(popt[0]),2))+'; f = '+str(round(float(popt[1]),2))+' ; phase ='+str(round(float(popt[2]),2))+' ; offset = '+str(round(float(popt[3]),2))


 # afficher points avec croix rouges. Inserer texte (titre, nom des axes,…)
 plt.figure()
 plt.scatter(t, acc, c = 'red', marker = '+')
 plt.plot(Xcalc,f(Xcalc,*popt),'g--',label = texte)
 plt.xlabel("t en s")
 plt.ylabel("a en g")
 plt.legend()   # pour afficher les légendes (label)
 plt.show()




 print (texte)
