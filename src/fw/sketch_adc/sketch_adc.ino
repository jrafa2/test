int sensorPin = A0;   // select the input pin
int sensorValue;

void setup() {
  Serial.begin(115200);
}

void loop() {
  while (Serial.available() > 0) {
    if (Serial.read() == 'r') {
      sensorValue = analogRead(sensorPin);  //float voltage = sensorValue * (5.0 / 1023.0);
      Serial.println(sensorValue);
    } 
  }
}
