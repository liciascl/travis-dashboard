#include <FastLED.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX, TX


#define NUM_LEDS 300


#define DATA_PIN 3


// Define the array of leds
CRGB leds[NUM_LEDS];
int state = 0;

void setup() { 

     FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
     mySerial.begin(115200);
     refresh_led("RGCRRGGCCGRR");
     delay(5000);
     refresh_led("OOOOOOOOOOOO");

}

void refresh_led(String str){
  int i=0;
  unsigned int led_counter = 0;
  while(str.length() > i && (led_counter<NUM_LEDS)){
    
    for(int j=0;j<33;j++){
      
      switch(str.charAt(i)){

        case 'R': leds[j+led_counter] = CRGB(255, 255, 00);
        break;
        case 'G': leds[j+led_counter] = CRGB(0, 255, 00);
        break;
        case 'C': leds[j+led_counter] = CRGB(120, 120, 00);
        break;
        case 'O': leds[j+led_counter] = CRGB(0, 0, 0);
        break;
        default:
          leds[j+led_counter] = CRGB(0, 0, 0);
        
      }

      led_counter +=1;
    }
    
    i+=1;

  }
  FastLED.show();
}
void loop() { 

//  Get string from Rpi
  if (mySerial.available()) {
      refresh_led(mySerial.readString());
  }
  
  delay(100);
}
