#include <Arduino.h>

// We communicate with the Arduino at 115200 baud.
#define SERIAL_BAUD 115200

#define FW_VER 1
const int trigPin = 11;
const int echoPin = 12;

const int trigDuration = 10;
const float soundSpeed = 0.343;// speed of sound in mm per ms
const int minDist = 70;
const int delayVal = 5;

const int redPin = 7;
const int greenPin = 6;
long duration;
int distance;

const int switchOut = 9;
const int switchIn = 10;

int state = 0;
void setup() {
  Serial.begin(SERIAL_BAUD);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);

  pinMode(switchOut, OUTPUT);
  pinMode(switchIn, INPUT);
}

int read_pin() {
  while (!Serial.available());
  int pin = Serial.read();
  return (int)(pin - 'a');
}

void command_read() {
  int pin = read_pin();
  // Read from the expected pin.
  int level = digitalRead(pin);
  // Send back the result indicator.
  if (level == HIGH) {
    Serial.write('h');
  } else {
    Serial.write('l');
  }
}

void command_analog_read() {
  int pin = read_pin();
  int value = analogRead(pin);
  Serial.print(value);
}

void command_write(int level) {
  int pin = read_pin();
  digitalWrite(pin, level);
}

void command_mode(int mode) {
  int pin = read_pin();
  pinMode(pin, mode);
}
void sensor_value(){ 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(trigDuration);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration * soundSpeed / 2); // distance in mm
  if (distance > minDist){
    digitalWrite(redPin, HIGH);
    digitalWrite(greenPin, LOW);
  }
  else if (distance <= minDist){
    if (distance > 0){
       digitalWrite(redPin, LOW);
       digitalWrite(greenPin, HIGH);
    }
  }
  Serial.print(distance);

}
void check_switches(){
  digitalWrite(switchOut, HIGH);
  state = digitalRead(switchIn);
  if (state == HIGH){
    Serial.print("True");
  }
  else{
    Serial.print("False");
  }
}
void loop() {
  // Fetch all commands that are in the buffer
  while (Serial.available()) {
    int selected_command = Serial.read();
    // Do something different based on what we got:
    switch (selected_command) {
      case 'a':
        command_analog_read();
        break;
      case 'r':
        command_read();
        break;
      case 'l':
        command_write(LOW);
        break;
      case 'h':
        command_write(HIGH);
        break;
      case 'i':
        command_mode(INPUT);
        break;
      case 'o':
        command_mode(OUTPUT);
        break;
      case 'p':
        command_mode(INPUT_PULLUP);
        break;
      case 'v':
        Serial.print("SRcustom:");
        Serial.print(FW_VER);
        break;
      case 's':
        sensor_value();
        break;
      case 'x':
        check_switches();
        break;
      default:
        // A problem here: we do not know how to handle the command!
        // Just ignore this for now.
        break;
    }
    Serial.print("\n");
  }
}
