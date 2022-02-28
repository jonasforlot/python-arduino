/*************************************************** 
 * Infrared CO2 Sensor0-5000ppm  
 * **************************************************** 
 * This example The sensors detect CO2 
 *  
 * @author lg.gang(lg.gang@qq.com) 
 * @version  V1.0 
 * @date  2016-7-6 
 *  
 * GNU Lesser General Public License. 
 * See <http://www.gnu.org/licenses/> for details. 
 * All above must be included in any redistribution 
 * ****************************************************/ 

 // intégration des capteurs d'humidité DHT11 et de CO2 par
 // Pierre Dieumegard, 4 décembre 2018
 // modifié par Jonas FORLOT 28 février pour utilisation avec shield LCD DF ROBOT
#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);
int sensorIn = A1;   
double total=0;
double totalA2=0;
float concentration = 0;

byte smiley_pas_content[8] = {
  B00000,
  B10001,
  B00000,
  B00000,
  B01110,
  B10001,
  B00000,
};

byte smiley_content[8] = {
  B00000,
  B10001,
  B00000,
  B00000,
  B10001,
  B01110,
  B00000,
};

byte smiley_moyen[8] = {
  B00000,
  B10001,
  B00000,
  B00000,
  B11111,
  B00000,
  B00000,
};

void setup(){   
  pinMode(11,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(2,OUTPUT);
  
  Serial.begin(9600);   
  // Set the default voltage of the reference voltage 
   analogReference (DEFAULT);
   lcd.begin(16,2);
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print("   Mesure   Concentration ");//Print a message to the LCD.
   lcd.setCursor(0, 1);
   lcd.print("               CO2  ");//Print a message to the LCD. 
  
   // déplacement de 16 position vers la droite
  for (int i = 0; i < 10; i++) {
    lcd.scrollDisplayLeft();
    delay(300);
  }
    
   delay (100);
} 


void loop(){  
  //Lecture de la tension pour CO2 
  int sensorValue = analogRead(sensorIn);  
 total=0;
 totalA2=0;
 for (int i=1; i <= 50; i++){
      total=total+analogRead(1)  ;
      totalA2=totalA2+analogRead(2)  ;
      delay(20); 
      }
     
  // Conversion en volts  
  float voltage = (total/50)*(5000/1024.0);  
  if(voltage == 0) 
  { 
    Serial.println("Problème"); 
    lcd.clear(); 
    lcd.print("Problème");
  } 
  else if(voltage < 400) 
  { 
        Serial.println("Préchauffage");
        lcd.clear(); 
        lcd.print("préchauffage"); 
  } 
  else 
  { 
    int voltage_diference=voltage-400; 
    float concentration=voltage_diference*50.0/16.0; 
    lcd.clear();
    //Print CO2 concentration 
    Serial.print("CO2: ");
    Serial.print(concentration);
    Serial.print(" ppm"); 
    

    //allumage des LED
  if  (concentration < 800) {   
    digitalWrite (2,HIGH);
    digitalWrite (3,LOW);
    digitalWrite (11,LOW);
    lcd.setCursor(0,0);
    lcd.print("CO2: ");
    lcd.print(concentration);
    lcd.print("ppm");
    lcd.createChar(0, smiley_content);
    lcd.setCursor(7,1);
    lcd.write(byte(0));
    
    delay(1000);
    
    
  }
else if  (concentration > 1600) {
    digitalWrite (2,LOW);
    digitalWrite (3,LOW);
    digitalWrite (11,HIGH);

    lcd.setCursor(0,0);
    lcd.print("CO2: ");
    lcd.print(concentration);
    lcd.print("ppm");
    lcd.createChar(0, smiley_pas_content);
    lcd.setCursor(7,1);
    lcd.write(byte(0));
    
    delay(1000);
    
    
    
    

  }
    

else {
    digitalWrite (2,LOW);
    digitalWrite (3,HIGH);
    digitalWrite (11,LOW);
     lcd.setCursor(0,0);
    lcd.print("CO2: ");
    lcd.print(concentration);
    lcd.print("ppm");
    lcd.createChar(0, smiley_moyen);
    lcd.setCursor(7,1);
    lcd.write(byte(0));
    
    delay(1000);
    
    
    
}
  }

    //maintenant la voie A2( facultative pour la lecture de CO2)
    
//    lcd.setCursor(0,1);
//    lcd.print("A2: ");
//    lcd.print(totalA2/50);
//    Serial.print("; A2: ");
//    Serial.print(totalA2/50);
//    Serial.print(" \n"); 
} 
