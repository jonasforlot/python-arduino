// Programme d'utilisation du capteur de pression avec Arduino avec carte SD

#include <SPI.h>
#include <SD.h>



//Définition des broches analogiques utilisées par le capteur.

#define _NUMER0_BROCHE_ANALOGIQUE A0          //Broche analogique utilisée par le capteur pression.
long temps;

File fichierSD;
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
// Procédure d'initialisation des périphériques
//==================================================================================================
void setup() {

  // Initialisation de la communication série avec le terminal à 9600 baud.
//  Serial.begin(9600);
  //  Initialisation de la carte SD
    if(!SD.begin(10)) {
//      Serial.println(F("Initialisation SD impossible !"));
    return;
    }
  
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


  // Lecture de la valeur du capteur sur l'entree analogique. 
  // La valeur mesurée par le Convertisseur Analogique Numérique prend pour valeur 0 pour une tension de 0V et 1023 pour une tension de 5V.
  int valeurNumerique = analogRead(_NUMER0_BROCHE_ANALOGIQUE);

  float tension_P_V   = ConvertiValeurMesureAnalogiqueEnTension(valeurNumerique);

  float pression_Pa = ConvertiTensionEnPression(tension_P_V);
  
  //Affichage des résultats
   fichierSD = SD.open("pression.txt", FILE_WRITE);
    if(fichierSD) {
    //     Serial.println(F("Ecriture en cours"));
   //Ecriture
      fichierSD.print(temps);
  
    fichierSD.print("\t");
    fichierSD.print(pression_Pa);
    fichierSD.println(""); 

    fichierSD.close();
  }
//  
//  Serial.print(" Pression : ");         // Transmission de la chaine " Pression:"
//  Serial.print(pression_Pa);          // Transmission de la pression absolue calculée.
//  Serial.println(" Pa");  
   

   
 
  
  delay(1000);                      // Délai en ms d'1s pour faciliter la visualisation.
}
