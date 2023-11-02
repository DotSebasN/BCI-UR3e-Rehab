const int Rele1 = 2; // Pin connected to LED 1
const int Rele2 = 3; // Pin connected to LED 2
const int Rele3 = 4; // Pin connected to LED 3
void setup() {
  pinMode(Rele1, OUTPUT); // Set LED 1 pin as an output
  pinMode(Rele2, OUTPUT); // Set LED 2 pin as an output
  pinMode(Rele3, OUTPUT); // Set LED 2 pin as an output
  digitalWrite(Rele1, HIGH); // Turn on LED 1
  digitalWrite(Rele2, HIGH);  // Turn off LED 2
  digitalWrite(Rele3, HIGH); // Turn off LED 3
  Serial.begin(57600); // Set the baud rate to match the communication 57600
}

void loop() {
  while (Serial.available()) {
    int c = Serial.read();

    if (c == '0') {
      digitalWrite(Rele1, LOW); // Turn on LED 1
      digitalWrite(Rele2, HIGH);  // Turn off LED 2
      digitalWrite(Rele3, HIGH); // Turn off LED 3
      delay(5000);
    } else if (c == '1') {
      digitalWrite(Rele1, HIGH);  // Turn off LED 1
      digitalWrite(Rele2, LOW); // Turn on LED 2
      digitalWrite(Rele3, HIGH); // Turn off LED 3
      delay(5000);
    } else if (c =='3') {
      digitalWrite(Rele1, HIGH);  // Turn off LED 1
      digitalWrite(Rele2, HIGH);  // Turn off LED 2
      digitalWrite(Rele3, LOW); // Turn on LED 3
      delay(5000);
    }
    digitalWrite(Rele1, HIGH); // Turn on LED 1
    digitalWrite(Rele2, HIGH);  // Turn off LED 2
    digitalWrite(Rele3, HIGH); // Turn off LED 3
  }
}
