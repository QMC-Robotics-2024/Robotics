const int trigPin = 11;
const int echoPin = 12;

const int trigDuration = 10;
const float soundSpeed = 0.343;// speed of sound in mm per ms
const int minDist = 100;
const int delayVal = 200;

const int redPin = 7;
const int greenPin = 6;
long duration;
int distance;
void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(trigDuration);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration * soundSpeed / 2); // distance in mm
  Serial.println(distance);

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
  delay(delayVal);
}
