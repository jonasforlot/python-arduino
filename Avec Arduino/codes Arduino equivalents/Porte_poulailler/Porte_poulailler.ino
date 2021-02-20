/*
Fermeture de la porte d’un poulailler pour un faible éclairement d'une photorésistance
*/
#include<Servo.h>

int Valeur_A0; 
float Tension_A0; 
Servo MonServo ;

void setup(){

MonServo.attach(9) ;
}

void loop(){
Valeur_A0=analogRead(A0); 
Tension_A0=(float)Valeur_A0*5/1023; 


if (Tension_A0<4.0){
 
MonServo.write(90) ;
}


else{

MonServo.write(45) ;
}
delay(250); 

}
