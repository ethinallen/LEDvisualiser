#include <FastLED.h>
#define numLED 550 //300 leds in strip/Users/andrewemery/Documents/html/aio_1.html
#define updateLED 8 //update 8 every millisecond
//Defined i/o pins
#define Pin 6
#define LED_TYPE    WS2812
#define COLOR_ORDER RGB
int rgb[3] = {0,0,0};
CRGB leds[numLED];

void setup() {
  FastLED.show();
  Serial.begin(9600);
  Serial.println("hello"); // specify baud rate
  int rgb[3];
  FastLED.addLeds<NEOPIXEL, Pin>(leds, numLED);
  for(int i = 0; i < numLED ; i++) {
      leds[i] = CRGB(0,0,0);
    }
  FastLED.show();
}

void loop() {
  unsigned long time = millis();

  // Shift to the right
  for(int i = numLED - 1; i >= updateLED; i --) {
    leds[i] = leds[i - updateLED];
  }
  
  // See if serial is communicating
  if (Serial.available() > 0) {
    // Assign serial written bytes to r, g, or b dependent on timing
     
    for(int j = 0; j < 3; j++) { //this writes the every third  value to r g b one at a time
      int incomingByte = Serial.read(); 
      Serial.println(incomingByte);
      rgb[j] = incomingByte;
    }
  }
   
  for(int i = 0; i < updateLED; i++) { 
    leds[i] = CRGB(rgb[0], rgb[1], rgb[2]);

  }
  FastLED.show();
  // clear this led for the next time around the loop
  delay(1);
}



