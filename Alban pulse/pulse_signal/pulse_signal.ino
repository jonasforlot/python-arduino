
int sign;
unsigned long temps;

//SETUP
void setup() {
  
  Serial.begin(9600);

  
 
}

void loop() {
  sign = analogRead(A0);
  temps = millis();
  Serial.print(temps);
  Serial.print("\t");
  
  Serial.println(sign);
  delay(100);

  
}
