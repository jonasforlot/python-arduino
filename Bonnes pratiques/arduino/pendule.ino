
float mesure ;               //délaration de la variable servant a stocker le signal lu
float angle ;
void setup() {
  Serial.begin (9600);        //démarrage de la communication série   
  }

void loop() {
  
     mesure = analogRead (A0); //on stocke la valeur analogique du potentiomètre dans la 
                              //variable mesure
    angle=0.176*mesure -90;
    
    Serial.print(millis());
    Serial.print("\t");    
    Serial.println(angle);
    
   
    
    delay (50);                     
  }
