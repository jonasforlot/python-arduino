// Programme d'utilisation du capteur de température et de pression avec Arduino.




//Définition des broches analogiques utilisées par le capteur.
#define _NUMER0_BROCHE_ANALOGIQUE_TENSION A1  //Broche analogique utilisée par le capteur pour la mesure de la tension aux bornes de la CTN
#define _NUMER0_BROCHE_ANALOGIQUE A0          //Broche analogique utilisée par le capteur pression.
long temps;
float R= 10000.0;
//==================================================================================================
// Convertit la valeur numérique en une valeur de tension.
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
// Convertit la valeur de la résistance de la CTN en une valeur de temperature.
// S'inspire de la méthode de Steinhart.
//==================================================================================================
float ConvertiResistanceEnTemperature(float resistance)
{
// Caracteristiques de la CTN  
const float _TEMPERATURE_NOMINALE = 25;
const float _THERMISTANCE_NOMINALE = 10000;
const float _COEFFICIENT_B = 3950; 
 
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
  temps = millis();
}



//==================================================================================================
// Convertit la valeur de tension en une valeur de pression.
// On mesure une tension de 0,2V pour une pression de  150hPa (un étalonnage du capteur montre que la tension de 0,2 V donnée par le constructeur pour 15 kPa peut varier légèrement ! On a choisi ici 0,27 )
// On mesure une tension de 4,7V pour une pression de 7000hPa.  
//==================================================================================================
float ConvertiTensionEnPression(float _tension)
{
// La fonction de conversion tension vers pression est de la forme pression = a * tension +b.  
const float _VALEUR_PRESSION_MIN= 150.0;
const float _VALEUR_TENSION_MIN = 0.27;
const float _VALEUR_PRESSION_MAX= 7000.0; //  
const float _VALEUR_TENSION_MAX = 4.7;
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
  temps= millis();
  // Lecture de la valeur tension du capteur sur l'entrée analogique _NUMER0_BROCHE_ANALOGIQUE_TENSION. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumeriqueTension = analogRead(_NUMER0_BROCHE_ANALOGIQUE_TENSION);
  // Conversion de la valeur numerique en tension.
  float tension_T_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumeriqueTension);
  
  
  // Calcul du courant , à partir de la tension aux bornes de la résistance de 10 kohms = Tension alimentation - tension CTN
  float courant_A   = (5.0 - tension_T_V)/R; //Calcul de l'intensité du courant en A
  //Calcul de la résistance de la CTN
  float resistance_ohm = tension_T_V / courant_A;

  //Appel de la méthode de la libraire pour la conversion de la résistance en température.
  float temperature_degreC= ConvertiResistanceEnTemperature(resistance_ohm);
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
  Serial.println(tension_T_V);    

   
 
  
  delay(5000);                      // Délai en ms d'1s pour faciliter la visualisation.
}
