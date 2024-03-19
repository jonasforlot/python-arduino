
 
 #define _NUMER0_BROCHE_ANALOGIQUE A8          //Broche analogique utilisée par le capteur pression. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).
int sensor = A0; // broche pour détection du capteur
 int etatSensor ; // état du capteur (haut ou bas)
 unsigned long start_time=0; //temps de début d'un comptage
 unsigned long end_time =0; //temps de fin d'un comptage
 int nb_trous =20 ; // nombre de trous de la roue codeuse
 bool etat_old= false ; // 
 bool  etat_new = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
 int compt=0; // comptage initialisé à 0
 float rps=0; // vitesse intialisée à 0
 long temps; //mesure du temps pour l'acquisition



 //==================================================================================================
 // Converti la valeur numérique en une valeur de tension.
 // Le Convertisseur Analogique Numérique converti la tension sur 10bits.  
 // Pour une tension de 0V la valeur numérique est 0.
 // Pour une tension de 5V la valeur numérique est 1023.  
 //==================================================================================================
 float ConvertiValeurMesureAnalogiqueEnTension(int _valeurNumerique)
 {
 // La fonction de conversion valeur numérique/tension est de la forme tension = a * valeurNumerique. 
 const int   _VALEUR_NUMERIQUE_MIN= 0;
 const float _VALEUR_TENSION_MIN  = 0.0;
 const int   _VALEUR_NUMERIQUE_MAX= 1023;   // convertisseur 10bits 
 const float _VALEUR_TENSION_MAX  = 5.0;
   //calcul du coefficient directeur
   float a = (_VALEUR_TENSION_MAX-_VALEUR_TENSION_MIN)/(_VALEUR_NUMERIQUE_MAX-_VALEUR_NUMERIQUE_MIN);
   //calcul de la tension
   float tension_V= a * _valeurNumerique; 
   return(tension_V);
 }
 //==================================================================================================
 // Converti la valeur de tension en une valeur de pression.
 // On mesure une tension de 0V pour une pression de  200hPa.
 // On mesure une tension de 5V pour une pression de 4000hPa.  
 //==================================================================================================
 float ConvertiTensionEnPression(float _tension)
 {
 // La fonction de conversion tension vers pression est de la forme pression = a * tension +b.  
 const float _VALEUR_PRESSION_MIN= 200.0;
 const float _VALEUR_TENSION_MIN = 0.0;
 const float _VALEUR_PRESSION_MAX= 4000.0; //  
 const float _VALEUR_TENSION_MAX = 5.0;
   // calcul du coefficient directeur
   float a = (_VALEUR_PRESSION_MAX-_VALEUR_PRESSION_MIN)/(_VALEUR_TENSION_MAX-_VALEUR_TENSION_MIN);
   // calcul du coefficient décalage à l'origine.
   float b = _VALEUR_PRESSION_MAX - a * _VALEUR_TENSION_MAX;
   //calcul de la pression
   float pression_Pa= (a * _tension) + b; // Pression en hecto Pascal.
   pression_Pa = pression_Pa * 100;       // Pression en Pascal
   return(pression_Pa);
 }

 
 void setup() 
 {
 pinMode(sensor,INPUT); // la broche A0est déclarée comme entrée
   Serial.begin(9600); // pour le moniteur série
   temps = millis(); // mesure du temps 
 }  
 void loop()
 {
 // Lecture de la valeur du capteur sur l'entree analogique. 
 // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
 int valeurNumerique = analogRead(_NUMER0_BROCHE_ANALOGIQUE);
 float tension_P_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumerique);
 float pression_Pa = ConvertiTensionEnPression(tension_P_V);
  compt = 0;
  start_time=millis(); //on mesure le temps
  end_time=start_time+1000; // pour un comptage toutes les secondes
  temps = millis(); //mesure du temps pour l'acquisition
 while(millis()<end_time){ // comptage sur une seconde
   if (analogRead(sensor)< 50){
     etat_new = true; 
   }
   else {
     etat_new =false;
   }
   if (etat_old != etat_new) {
     etat_old = etat_new;
     compt = compt + 1;
   }
 }
 rps = float(compt)/(2*nb_trous) ; // il faut diviser par 2 car pour chaque trou , deux changements d'état vont être détectés

 Serial.print(temps);
 Serial.print("\t");
 Serial.print(rps);
 Serial.print("\t");         
 Serial.println(pression_Pa);          
 }
