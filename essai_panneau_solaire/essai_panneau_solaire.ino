#include<Servo.h>

int ValEO; 
int ValNS; 
float Tension_EO; 
float Tension_NS; 
int angleEO=90;
int angleNS=90;
Servo MonServo1 ;
Servo MonServo2 ;

void setup(){


MonServo1.attach(9) ;
MonServo2.attach(10) ;

MonServo1.write(angleEO);
MonServo2.write(angleNS);
Serial.begin(9600);
}

void loop(){
ValEO=analogRead(A0); 
Tension_EO=(float)ValEO*5.0/1023; 
ValNS=analogRead(A1); 
Tension_NS=(float)ValNS*5.0/1023; 
delay(5);

if ((angleNS<200) and (angleEO <200) and  (angleEO > 10) and  (angleNS > 10)){

if (ValEO>512){
angleEO += 1;

}

else{
angleEO -= 1;
}

if (ValNS<512){
 angleNS += 1;

}

else{
angleNS -= 1;
}

MonServo1.write(angleEO) ;
MonServo2.write(angleNS) ;

}

  else {
    angleNS = 90;
    angleEO = 90;
    MonServo1.write(angleEO) ;
    MonServo2.write(angleNS) ;
    delay(100);
  }
 delay(50);
Serial.print(" E0:");   
 Serial.println(ValEO);  
 Serial.print(" NS:");   
 Serial.println(ValNS); 
 Serial.print("Angle E0:");   
 Serial.println(angleEO); 
 Serial.print("Angle NS:");   
 Serial.println(angleNS); 


}

  
