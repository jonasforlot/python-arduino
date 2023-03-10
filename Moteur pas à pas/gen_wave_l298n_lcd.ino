#include <EEPROM.h>


// Include the Arduino Stepper Library
#include <Stepper.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);

// Number of steps per output rotation
const int stepsPerRevolution = 200;
float  freqmoteur ;
int rpm ;

int valeur_bouton;

// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 2,3,11,12);


void setup()
{
 
  // initialize the serial port:
  Serial.begin(9600);
  EEPROM.get(0,freqmoteur);
   lcd.begin(16,2);
}

void loop() 
{
 valeur_bouton  = analogRead(A0);
  if (valeur_bouton ==205 or valeur_bouton ==204 or valeur_bouton ==203) {
  freqmoteur+=0.1;
  EEPROM.put(0, freqmoteur);
  delay(2);
}
if (valeur_bouton == 405 or valeur_bouton ==401 or valeur_bouton == 402) {
  freqmoteur-=0.1;
  EEPROM.put(0, freqmoteur);
  delay(2);
}
EEPROM.get(0,freqmoteur);
if (freqmoteur > 4.0) {
      EEPROM.get(0,freqmoteur);
}
else{
  freqmoteur = 4.0;
  EEPROM.put(0, freqmoteur);
}
Serial.println(rpm);
lcd.setCursor(0,0);
lcd.print("Freq moteur");
lcd.setCursor(5,1);
lcd.print(freqmoteur,1);
lcd.setCursor(10,1);
lcd.print("Hz");
rpm =int(freqmoteur*60);
//  Serial.println("clockwise");

   // set the speed :
  
  myStepper.setSpeed(rpm);
  // step one revolution in one direction:

  myStepper.step(stepsPerRevolution);
  
  
}
