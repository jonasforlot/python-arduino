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

  while(true)
  { 
    Valeur_alim = analogRead(broche_alim); // Valeur comprise entre 0 et 1023
    U_alim = Valeur_alim *5.0/1023; // Calcul de la tension U_alim
    Valeur_LDR   = analogRead(broche_LDR); // Valeur comprise entre 0 et 1023
    U_LDR = (float)Valeur_LDR*5/1023; //Calcul de la tension aux bornes de la photorésistance
    
    delay(1000);       // Délai en ms pour la stabilisation de la tension 
                       //pour la mesure de résistances.
    
   
    float courant_A   = (U_alim - U_LDR)/R; //Calcul de l'intensité du courant en A

    //Affichage des resultats


    Serial.print(" Tension LDR: ");   // Affichage de la tension en V sur le moniteur série
    Serial.print(U_LDR);            
    Serial.print(" V");              
  
    Serial.print(" Courant: ");          // Affichage du courant en mA sur le moniteur série
    Serial.print(courant_A*1000);       
    Serial.print(" mA");                
    
    Serial.println("");                 // Saut de ligne.

  }
}
  
