
#define LED_PIN 13

int msgByte= -1;         // incoming byte
const int msgSize = 50;  // max message size
char msgArray[msgSize];  // array for incoming data
int msgPos = 0;          // current position

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    handleSerial();
}

void handleSerial() {  
  if (Serial.available() > 0) {
  	digitalWrite(LED_PIN, HIGH);
    msgByte = Serial.read();
    
    if (msgByte != '\n') {
      // add incoming byte to array
      msgArray[msgPos] = msgByte;
      msgPos++;
    } else {
      // reached end of line
      msgArray[msgPos] = 0;
      
      // here the message is processed
      // for now just send it back over serial
      Serial.println(msgArray);
    
      // reset byte array
      for (int c = 0; c < msgSize; c++) 
        msgArray[c] = ' ';

      msgPos = 0;
      digitalWrite(LED_PIN, LOW);
    }
  }
}