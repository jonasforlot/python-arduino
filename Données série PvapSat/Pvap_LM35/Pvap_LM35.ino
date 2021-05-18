// Programme pour mesures température et pression
// Ce capteur mesure la température de -40 à 200 °C
// On utilise un capteur de pression Eurosmart et un capteur de température LM35 

//Définition des broches analogiques utilisées par le capteur.
#define _NUMER0_BROCHE_ANALOGIQUE_LM35 A0 //Broche analogique utilisée par le capteur pour la mesure du courant. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).
#define _NUMER0_BROCHE_ANALOGIQUE A8          //Broche analogique utilisée par le capteur pression. (Dépend de la localisation du capteur sur la carte EDUCA DUINO Lab).

 long temps;

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
// Convertit la valeur de la tension aux bornes de la LM35 en température en °C
//==================================================================================================
float ConvertiTensionEnTemperature(float tension)
{

  float temperature = tension*100;

  return(temperature);
}


//==================================================================================================
// Procédure d'initialisation des périphériques
//==================================================================================================
void setup() {
  // Initialisation de la communication série avec le terminal à 9600 baud.
  Serial.begin(9600);
  temps = millis();
}



//==================================================================================================
// Convertit la valeur de tension en une valeur de pression.
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
 temps = millis();
  // Lecture de la valeur tension du capteur sur l'entrée analogique _NUMER0_BROCHE_ANALOGIQUE_TENSION. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumeriqueTension = analogRead(_NUMER0_BROCHE_ANALOGIQUE_LM35);
  // Conversion de la valeur numerique en tension.
  float tension_T_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumeriqueTension);
  

  //Appel de la méthode de la libraire pour la conversion de la résistance en température.
  float temperature_degreC= ConvertiTensionEnTemperature(tension_T_V);

  //Affichage des résultats
  Serial.print("t : ");
  Serial.print("\t");
  Serial.print(temps); 
  
  Serial.print(" Temp : ");    // Transmission de la chaine " Température:"
  Serial.print(temperature_degreC); // Transmission de la temperature en °C
  Serial.print(" degresC ");              // Transmission de l'unité.
  
  
  // Lecture de la valeur du capteur sur l'entree analogique. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumerique = analogRead(_NUMER0_BROCHE_ANALOGIQUE);

  float tension_P_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumerique);

  float pression_Pa = ConvertiTensionEnPression(tension_P_V);
  
  //Affichage des résultats
  
  
  Serial.print(" Pression : ");         // Transmission de la chaine " Pression:"
  Serial.print(pression_Pa);          // Transmission de la pression absolue calculée.
  Serial.println(" Pa");    

  
  delay(1000);                      // Délai en ms d'1s pour faciliter la visualisation.
}
