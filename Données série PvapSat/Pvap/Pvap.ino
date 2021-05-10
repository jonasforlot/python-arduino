// Programme d'utilisation du capteur de température Eurosmart Elab_Temp.
// Ce capteur mesure la température de -40 à 200 °C
// Le capteur utilise 2 broches analogiques de la carte EDUCA DUINO Lab pour les mesures de tension et de courant.
// Les mesures effectuées sont transmises via la laison série.
// Elles peuvent être visualisées par le terminal intégré d'Arduino par le menu [Outil][Moniteur Série]

//Définition des broches analogiques utilisées par le capteur.
#define _NUMER0_BROCHE_ANALOGIQUE_TENSION A12  //Broche analogique utilisée par le capteur pour la mesure de la tension. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).
#define _NUMER0_BROCHE_ANALOGIQUE_COURANT A13 //Broche analogique utilisée par le capteur pour la mesure du courant. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).
#define _NUMER0_BROCHE_ANALOGIQUE A8          //Broche analogique utilisée par le capteur pression. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).


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
// Converti la valeur numérique en une valeur de tension.
// Le Convertisseur Analogique Numerique converti en un courant.  
// Le courant est determiné par la mesure d'une tension aux bornes d'une résistance de 10kOhms
//==================================================================================================
float ConvertiValeurMesureAnalogiqueEnCourant(int _valeurNumerique)
{
const float _RESISTANCE = 10000.0; //Résistance de 10kOhms    
  // Conversion de la valeur numérique en tension
  float tension_V= ConvertiValeurMesureAnalogiqueEnTension(_valeurNumerique); 
  float courant_A= tension_V / _RESISTANCE;
  return(courant_A);
}

//==================================================================================================
// Converti la valeur de la résistance de la CTN en une valeur de temperature.
// S'inspire de la méthode de Steinhart.
//==================================================================================================
float ConvertiResistanceEnTemperature(float resistance)
{
// Caracteristiques de la CTN  
const float _TEMPERATURE_NOMINALE = 25;
const float _THERMISTANCE_NOMINALE = 150;
const float _COEFFICIENT_B = 3090; 
 
  float temperature = resistance/ _THERMISTANCE_NOMINALE;
  temperature = log(temperature);
  temperature /= _COEFFICIENT_B;
  temperature += 1.0 /(_TEMPERATURE_NOMINALE + 273.15);
  temperature = 1.0 /temperature;
  temperature -= 273.15;
  return(temperature);
}


//==================================================================================================
// Procédure d'initialisation des périphériques
//==================================================================================================
void setup() {
  // Initialisation de la communication série avec le terminal à 9600 baud.
  Serial.begin(9600);
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

//==================================================================================================
// Boucle principale Arduino.
//==================================================================================================
void loop() {

  // Lecture de la valeur tension du capteur sur l'entrée analogique _NUMER0_BROCHE_ANALOGIQUE_TENSION. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumeriqueTension = analogRead(_NUMER0_BROCHE_ANALOGIQUE_TENSION);
  // Conversion de la valeur numerique en tension.
  float tension_T_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumeriqueTension);
  
  // Lecture de la valeur courant du capteur sur l'entree analogique _NUMER0_BROCHE_ANALOGIQUE_TENSION. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  // Le courant est déterminé par la mesure de la tension aux bornes d'une résistance de 10kOhms.
  int valeurNumeriqueCourant = analogRead(_NUMER0_BROCHE_ANALOGIQUE_COURANT);
  // Conversion de la valeur numérique en courant.
  float courant_A   = ConvertiValeurMesureAnalogiqueEnCourant(valeurNumeriqueCourant);

  //Calcul de la résistance
  float resistance_ohm = tension_T_V / courant_A;

  //Appel de la méthode de la libraire pour la conversion de la résistance en température.
  float temperature_degreC= ConvertiResistanceEnTemperature(resistance_ohm);

  //Affichage des résultats
  Serial.print(" Valeur num Tension:");        // Transmission de la chaine " Tension:"
  Serial.print(valeurNumeriqueTension);          // Transmission de la tension en V.
  Serial.print(" ");   

 Serial.print(" Valeur num Courant:");        // Transmission de la chaine " Tension:"
  Serial.print(valeurNumeriqueCourant);          // Transmission de la tension en V.
  Serial.print(" ");  
  
  Serial.print(" Tension:");        // Transmission de la chaine " Tension:"
  Serial.print(tension_T_V);          // Transmission de la tension en V.
  Serial.print(" V");               // Transmission de l'unité.
  
  Serial.print(" Courant:");        // Transmission de la chaine " Courant:"
  Serial.print(courant_A*1000);     // Transmission de la valeur du courant en mA.
  Serial.print(" mA");              // Transmission du multiple et de l'unité.
  
  Serial.print(" Résistance:");     // Transmission de la chaine " Résistance:"
  Serial.print(resistance_ohm);     // Transmission de la valeur de la résistance en ohm
  Serial.print(" Ohms");             // Transmission de l'unité. Caractère ohm non disponible.

  Serial.print(" Température:");    // Transmission de la chaine " Température:"
  Serial.print(temperature_degreC); // Transmission de la temperature en °C
  Serial.print(" °C");              // Transmission de l'unité.
  
  Serial.println("");               // Saut de ligne.


  // Lecture de la valeur du capteur sur l'entree analogique. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumerique = analogRead(_NUMER0_BROCHE_ANALOGIQUE);

  float tension_P_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumerique);

  float pression_Pa = ConvertiTensionEnPression(tension_P_V);
  
  //Affichage des résultats
  Serial.print("Valeur numerique:");  // Transmission de la chaine "Valeur numerique:"
  Serial.print(valeurNumerique);      // Transmission de la valeur numérique fournie par le Convertisseur Analogique Numérique
  
  Serial.print(" Tension:");          // Transmission de la chaine " Tension:"
  Serial.print(tension_P_V);            // Transmission de la tension calculée.
  Serial.print(" V");                 // Transmission de l'unité.
  
  Serial.print(" Pression:");         // Transmission de la chaine " Pression:"
  Serial.print(pression_Pa);          // Transmission de la pression absolue calculée.
  Serial.println(" Pa");    

  
  delay(1000);                      // Délai en ms d'1s pour faciliter la visualisation.
}
