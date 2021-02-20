/*
Allumage d'une LED pour un faible éclairement d'une photorésistance
*/


int Valeur_A0; 
float Tension_A0; 


void setup(){

pinMode(2,OUTPUT) ;  }


void loop(){
Valeur_A0=analogRead(A0); Tension_A0=(float)Valeur_A0*5/1023; 
if (Tension_A0<4.0){

 digitalWrite(2,HIGH); 
}


else{

 digitalWrite(2,LOW) ; }

delay(250); 

}
