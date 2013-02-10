
#define LED_PIN 13

void setup()
{
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    digitalWrite(LED_PIN, HIGH);
    Serial.println("{'heading': 45}");
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(1900);
}
