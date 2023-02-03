const int pinBobine1A = 8 ;
const int pinBobine1C = 9 ;
const int pinBobine2B = 10 ;
const int pinBobine2D = 11 ;


float Tps =8;
int Tour=0; // Déclaration variable nombre de tour

void setup() {
  pinMode(pinBobine1A, OUTPUT); // 
  pinMode(pinBobine1C, OUTPUT); // 
  pinMode(pinBobine2B, OUTPUT); // 
  pinMode(pinBobine2D, OUTPUT); //

  

  Serial.begin(9600);
}




void loop(){
  sens_normal();
  stop();
  delay(100);
  sens_inverse();
  delay(100);
  sens_inverse();
  delay(100);
  


 
}

void sens_normal(){
  for (Tour = 0; Tour < 50; Tour++){ // Boucle pour faire 1 tour complet (Moteur 200 pas/4 = 50)
// Commande moteur pas à pas Bipolaire 4 fils en Mode Wave | Sens Normal
// Pas n°1 | 
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, HIGH);  
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, LOW);

delay(Tps);
  
// Pas n°2 | 
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, LOW);   
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, HIGH);
delay(Tps); 

// Pas n°3 | 
digitalWrite(pinBobine1A, HIGH);
digitalWrite(pinBobine1C, LOW);  
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, LOW);
delay(Tps); 

// Pas n°4 | 
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, LOW);   
digitalWrite(pinBobine2B, HIGH);
digitalWrite(pinBobine2D, LOW);
delay(Tps); 
 }

  
}


void sens_inverse(){
 for (Tour = 0; Tour < 50; Tour++){ // Boucle pour faire 1 tour complet (Moteur 200 pas/4 = 50)
// Commande moteur pas à pas Bipolaire 4 fils en Mode Wave | Sens Inverse
// Pas n°1 |
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, LOW);   
digitalWrite(pinBobine2B, HIGH);
digitalWrite(pinBobine2D, LOW);
delay(Tps); 


// Pas n°2 |
digitalWrite(pinBobine1A, HIGH);
digitalWrite(pinBobine1C, LOW);  
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, LOW);
delay(Tps); 

// Pas n°3 |
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, LOW);   
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, HIGH);
delay(Tps); 

// Pas n°4 |
digitalWrite(pinBobine1A, LOW);
digitalWrite(pinBobine1C, HIGH);  
digitalWrite(pinBobine2B, LOW);
digitalWrite(pinBobine2D, LOW);
delay(Tps); 

delay(Tps);
  




  }
  
}

void stop(){
    digitalWrite(pinBobine1A, LOW);
     digitalWrite(pinBobine1C, LOW);  
     digitalWrite(pinBobine2B, LOW);
     digitalWrite(pinBobine2D, LOW);
}

  
