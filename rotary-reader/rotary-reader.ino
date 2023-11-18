volatile long encoderPos_1 = 0;
volatile long encoderPos_2 = 0;
int encoder_1_PinA = 2;
int encoder_1_PinB = 4;
int encoder_2_PinA = 3;
int encoder_2_PinB = 5;
int _switch = 6;
int encoderPinALast_1 = LOW;
int encoderPinALast_2 = LOW;
int n = LOW;
int switch_state = HIGH;

void setup() {
  pinMode(encoder_1_PinA, INPUT);
  pinMode(encoder_1_PinB, INPUT);
  pinMode(encoder_2_PinA, INPUT);
  pinMode(encoder_2_PinB, INPUT);
  pinMode(_switch, INPUT_PULLUP);
  Serial.begin(9600);
  // Attach interrupts
  attachInterrupt(digitalPinToInterrupt(encoder_1_PinA), readEncoder_1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoder_2_PinA), readEncoder_2, CHANGE);
  encoderPinALast_1 = digitalRead(encoder_1_PinA);
  encoderPinALast_2 = digitalRead(encoder_2_PinA);
}

void loop() {
  // Send encoder position over serial port
  Serial.print(encoderPos_1);
  Serial.print(",");
  Serial.println(encoderPos_2);
  int sw = digitalRead(_switch);
  if (sw != switch_state) {
    switch_state = sw;
    if (switch_state == LOW) {
      Serial.println("switch");
    }else{
      Serial.println("release");
    }
  }
}

void readEncoder_1() {
  int aVal = digitalRead(encoder_1_PinA);
  int bVal = digitalRead(encoder_1_PinB);

  if (aVal != encoderPinALast_1) {
    if (aVal != bVal) {
      encoderPos_1 ++;
    } else {
      encoderPos_1 --;
    }
  }

  encoderPinALast_1 = aVal;

}

void readEncoder_2() {
  int aVal = digitalRead(encoder_2_PinA);
  int bVal = digitalRead(encoder_2_PinB);

  if (aVal != encoderPinALast_2) {
    if (aVal != bVal) {
      encoderPos_2 ++;
    } else {
      encoderPos_2 --;
    }
  }

  encoderPinALast_2 = aVal;

}

