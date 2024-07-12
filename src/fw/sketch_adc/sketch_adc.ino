#include <avr/sleep.h>

int sensorPin = A0;   // select the input pin
int sensorValue;

void setup() {
  Serial.begin(115200);
  analogRead(sensorPin);  //dummy read
}

char read_char;
void loop() {
  while (Serial.available() > 0) {
    read_char = Serial.read();
    if (read_char == 'r') {
      sensorValue = analogRead(sensorPin);  //float voltage = sensorValue * (5.0 / 1023.0);
      Serial.println(sensorValue);
    }  
    if (read_char == 't') {
      sensorValue = getTemp();  //float voltage = sensorValue * (1.1 / 1023.0);
      Serial.println(sensorValue - 342);  //ºC
      delay(500);
      analogRead(sensorPin);  //dummy read
      delay(2000);
    } 
  }
}

//https://forum.arduino.cc/t/using-the-internal-temperature-sensor/8201/9
int getTemp(){
  ADMUX = 0xC8; // turn on internal reference, right-shift ADC buffer, ADC channel = internal temp sensor
  delay(10);

  // start the conversion
   ADCSRA |= _BV(ADSC);
    
  // ADSC is cleared when the conversion finishes
  while (bit_is_set(ADCSRA, ADSC));

   return (ADCL | (ADCH << 8))  ;
}
