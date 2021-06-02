# -*- coding: utf-8 -*-


import pycanum.main as pycan
import matplotlib.pyplot as plt
import numpy
import math
import numpy.fft
import scipy.signal
import os


# prÃ©fixe pour les noms des fichiers de sauvegarde
nom = "signal-2"
# ouverture de l'interface pour SysamSP5
can = pycan.Sysam("SP5")
# configuration des entrÃ©es 0 et 1 avec un calibre 10.0 V
can.config_entrees([0],[10])

# FrÃ©quence d'Ã©chantillonnage (max 10 MHz)
fe=20000.0
te=1.0/fe
# durÃ©e de l'acquisition
T=5.0
# nombre d'Ã©chantillons (Max 130000 environ)
N = int(T/te)
print(N)
# configuration de l'Ã©chantillonnage. La pÃ©riode d'Ã©chantillonnage est donnÃ©e en microsecondes
can.config_echantillon(te*10**6,N)
# acquisition
can.acquerir()
# Lecture des instants et des tensions pour la voie 0 et la voie 1
t=can.temps()
u=can.entrees()
t0=t[0]
u0=u[0]

# fermeture de l'interface
can.fermer()

# On relie la pÃ©riode d'Ã©chantillonnage et la durÃ©e Ã  partir des donnÃ©es
# car il peut y avoir une diffÃ©rence avec les valeurs spÃ©cifiÃ©es au dÃ©part
te = t0[1]-t0[0]
fe = 1.0/te
N = t0.size
T = t0[N-1]-t0[0]


listeTemps = list(t0)
listeEA0 = list(u0)





# numpy.savetxt('entreeDirecte-data-1.txt',[listeTemps,listeEA0,listeEA1])


plt.figure()
plt.plot(listeTemps,listeEA0,color='#FF0000', linestyle='dotted', label="U=(t)")
plt.axis([0,0.5,-10.0,10.0])
plt.xlabel("t (s)")
plt.ylabel("U (V)")
plt.grid()
plt.legend()
plt.savefig("signal.pdf")
plt.show()

#Ecriture dans un fichier txt
lines=['t\tU\n'] #première ligne du fichier txt
for i in range (len (listeEA0)):
    line = str(listeTemps[i]) +'\t'+ str(listeEA0[i])+'\n'
    lines.append(line)

fichier = open('P:\Mes documents\Essai Sysam Python\data_micro.txt', 'w').writelines(lines) #création d'un nouveau fichier texte




