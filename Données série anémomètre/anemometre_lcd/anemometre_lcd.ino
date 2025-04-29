/*!
 * @file  SEN0170.ino
 * @brief Reading wind speed rating
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license  The MIT License (MIT)
 * @author  DFRobot
 * @version  V1.0
 * @date  2023-08-03
 */
#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);

long temps;

void setup()
{
  Serial.begin(9600);
  lcd.begin(16,2);
}

void loop()
{
  temps = millis();
  int sensorValue = analogRead(A1);
  float outvoltage = sensorValue * (5.0 / 1023.0);
//  Serial.print("outvoltage = ");
//  Serial.print(outvoltage);
//  Serial.println("V");
  float Level = 6.0 * outvoltage;//The level of wind speed is proportional to the output voltage.
//  Serial.print("wind speed is ");
  Serial.print(temps);
  Serial.print("\t");
  Serial.println(Level);
  lcd.setCursor(0,0);
  lcd.print("Vitesse : ");
  lcd.setCursor(0,1);
  lcd.print(Level);
  lcd.setCursor(8,1);
  lcd.print(" ");
  lcd.setCursor(9,1);
  lcd.print("m/s");
  
//  Serial.println(" m/s");
//  Serial.println();
  delay(50);
}
