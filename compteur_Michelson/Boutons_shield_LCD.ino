

#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);

int valeur_bouton;




void setup() 
{
  
  Serial.begin(9600); // pour le moniteur série
  lcd.begin(16,2);
  
}  
 
void loop()
{

valeur_bouton  = analogRead(A0);
Serial.println(valeur_bouton);
lcd.clear();
lcd.setCursor(0,0);
lcd.print(valeur_bouton);

 delay(10);
}
