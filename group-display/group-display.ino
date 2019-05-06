#include <FastLED.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX
#define GROUPS 12

#define NUM_LEDS 282
//the sum of ledPerGroup has to be the same as NUM_LEDS
byte ledPerGroup[] = {24, 24, 25, 25, 24, 24, 23, 25, 25, 25, 25, 13};

#define DATA_PIN 3

// Define the array of leds
CRGB leds[NUM_LEDS];
int state = 0;
String incomingString = "";
void setup() {

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  mySerial.begin(115200);
  Serial.begin(115200);

  refresh_led("RRRGRRRRORRR");
 
}

void refresh_led(String str) {
  int len = str.length();
  Serial.println(str);
  Serial.println(len);

  int i = 0;
  int led_counter = 0;

  for (int j = 0; j < len; j++) {
    Serial.println(ledPerGroup[j]);

    for (int i = 0; i < ledPerGroup[j]; i++) {
      switch (str[j]) {

      case 'R':
        leds[i + led_counter] = CRGB(120, 0, 00);
        break;
      case 'G':
        leds[i + led_counter] = CRGB(0, 120, 00);
        break;
      case 'C':
        leds[i + led_counter] = CRGB(0, 120, 50);
        break;
      case 'O':
        leds[i + led_counter] = CRGB(0, 0, 0);
        break;
      default:
        leds[i + led_counter] = CRGB(0, 0, 0);
      }
    }
    led_counter += ledPerGroup[j];
  }

  FastLED.show();
}

void refresh_led_test() {

  int i = 0;
  int led_counter = 0;
  while (NUM_LEDS >= i) {

    leds[i] = CRGB(0, 0, 120);

    i++;
  }

  FastLED.show();
}

void loop() {
  
  //    Get string from Rpi
  if (mySerial.available()>0) {

    incomingString = mySerial.readString();
    refresh_led(incomingString);
    
  }

  delay(100);
}
