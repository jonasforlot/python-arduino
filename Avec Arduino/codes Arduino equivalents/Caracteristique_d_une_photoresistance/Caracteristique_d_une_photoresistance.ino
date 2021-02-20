
float R= 1000;
int const broche_LDR = A0;
int const broche_alim = A1;
int Valeur_LDR;
int Valeur_alim;
float U_alim;
float U_LDR;

//==================================================================================================
// Procédure d'initialisation des périphériques
//==================================================================================================
void setup() {
  // Initialisation de la communication série avec le terminal à 9600 baud.
  Serial.begin(9600);
  
}


//==================================================================================================
// Boucle principale Arduino.
//==================================================================================================
void loop() {





  // Mesures de la tension U_LDR en faisant varier U_alim avec le potentiomètre
  while( U_alim < 5.0)
  { 
    
    Valeur_alim = analogRead(broche_alim); 
    U_alim = Valeur_alim *5.0/1023;
    Valeur_LDR   = analogRead(broche_LDR);
    U_LDR = (float)Valeur_LDR*5/1023;
    
    delay(1000);                           // Délai en ms pour la stabilisation de la tension pour la mesure de résistances.
    
   
    float courant_A   = (U_alim - U_LDR)/R;

    //Affichage des resultats

    Serial.print(" Tension LDR: ");               // Transmission de la chaine " Tension:"
    Serial.print(U_LDR);               // Transmission de la tension en V mesurée aux bornes de la résistance..
    Serial.print(" V");                      // Transmission de l'unité.
  
    Serial.print(" Courant: ");               // Transmission de la chaine " Courant:"
    Serial.print(courant_A*1000);            // Transmission de la valeur du courant en mA circulant à travers la résistance.
    Serial.print(" mA");                     // Transmission de l'unité.
    
    Serial.println("");                      // Saut de ligne.

  }//FinFor consigneTension

  Serial.print("Fin de la session de mesures");// Transmission de la chaine "Fin de la cession de mesures"

  // Arrêt des mesures. A mettre en commentaire si on souhaite plusieur série de mesures.
  while(1);           
}
