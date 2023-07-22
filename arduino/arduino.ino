// DHT11 library
#include "DHT.h"

const int DHTPIN = 2;        // Read data from DHT11 at D2 in Arduino Board
const int DHTTYPE = DHT11;   // Declare Sensor Type: DHT11 and DHT22
const int outPin = 4;        // D4 for monitoring and controlling Motor
const int thresholdTmp = 27; // Threshold of temperature for running or stopping motor

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(9600);
  dht.begin(); // Start Sensor
  pinMode(outPin, OUTPUT);
}

void checkTemperature(float t)
{
  if (t > thresholdTmp)
  {
    digitalWrite(outPin, HIGH);
  }
  else
  {
    digitalWrite(outPin, LOW);
  }
}

void exportSerialPort(float h, float t, bool motorFbk)
{
  // Export temperature, Humidity, motor feedback by serial port
  Serial.print(t);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.print(digitalRead(outPin));
  Serial.println();
}

void getData(float &h, float &t, bool &motorFbk)
{
  // Get temperature, Humidity, motor feedback
  h = dht.readHumidity();
  t = dht.readTemperature();
  motorFbk = digitalRead(outPin);
}

void loop()
{
  float h, t;
  bool motorFbk;
  getData(h, t, motorFbk);
  checkTemperature(t);
  exportSerialPort(h, t, digitalRead(outPin));
  delay(1000); // Wait 1 second
}
