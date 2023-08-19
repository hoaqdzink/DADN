// DHT11 library
#include "DHT.h"

const int DHTPIN = 2;        // Read data from DHT11 at D2 in Arduino Board
const int DHTTYPE = DHT11;   // Declare Sensor Type: DHT11 and DHT22
const int outPin = 4;        // D4 for monitoring and controlling Motor
const int ledPin = 8;        // D7 for controlling Led
const int thresholdTmp = 35; // Threshold of temperature for running or stopping motor
const int ledThresholdTmp = 30; // Threshold of temperature for turning led on
int userType = 0;            // Mode: 0:Manually, Mode: 1:Automatically

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
  Serial.begin(9600);
  dht.begin(); // Start Sensor
  pinMode(outPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
}

void stopMotor()
{
  digitalWrite(outPin, LOW);
}

void startMotor()
{
  digitalWrite(outPin, HIGH);
}

void turnLedOn()
{
  digitalWrite(ledPin, HIGH);
}

void turnLedOff()
{
  digitalWrite(ledPin, LOW);
}

void checkTemperature(float t)
{
  if (userType == 1)
  {
    if (t > thresholdTmp)
    {
      startMotor();
    }
    else
    {
      stopMotor();
    }
  }
  if (t > ledThresholdTmp)
    {
      turnLedOn();
    }
    else
    {
      turnLedOff();
    }
}

void exportSerialPort(float h, float t, bool motorFbk)
{
  // Export temperature, Humidity, motor feedback by serial port
  Serial.print(t);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.print(motorFbk);
  Serial.println();
}

void getData(float &h, float &t, bool &motorFbk)
{
  // Get temperature, Humidity, motor feedback
  h = dht.readHumidity();
  t = dht.readTemperature();
  motorFbk = digitalRead(outPin);
}

void processReadSerial()
{
  String serialRead;
  serialRead = Serial.readString();
  if (serialRead[0] == '0')
  {
    if (serialRead[1] == '0')
      stopMotor();
    if (serialRead[1] == '1')
      startMotor();
  }
  if (serialRead[0] == '1')
  {
    if (serialRead[1] == '0')
      userType = 0;
    if (serialRead[1] == '1')
      userType = 1;
  }
}

void loop()
{
  float h, t;
  bool motorFbk;
  getData(h, t, motorFbk);
  checkTemperature(t);
  exportSerialPort(h, t, motorFbk);
  processReadSerial();
  delay(1000); // Wait 1 second
}
