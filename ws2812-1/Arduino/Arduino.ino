#include "Adafruit_NeoPixel.h"

#define PIN 2
#define NUMPIXELS 31
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
uint16_t hh = 0;
const String hexDigits = "0123456789ABCDEF";

void setup(){
    pixels.begin();
    pixels.setBrightness(255);
    Serial.begin(250000);
    pinMode(13, OUTPUT);
}
bool flag = 0;
String data;
String color_str[31];

void loop(){
    /*
    for(int64_t i = 0; i < 120; i++){
        pixels.setPixelColor(119-i, pixels.ColorHSV((hh+(2800*i))%65536, 255, 255));
    }
    pixels.show();
    delay(10);
    hh += 350;
    */
    if(Serial.available()){
        data = Serial.readStringUntil('M'); ///Serial.readString()
        if(data == "get device name"){
            Serial.print("ws2812-1");
            pinMode(13, HIGH);
        }
        else{
            flag = 1;
        }
    }
    if(flag){
        //Serial.println(data);
        int nn = data.indexOf('m');
        String data__ = data.substring(nn+2);
        for(int i = 0; i < 31; i++){
            String degT = data__.substring(i*7, i*7+6);
            color_str[i] = degT;
            long result = 0;
            color_str[i].toUpperCase();
            for (int j = 0; j < color_str[i].length(); j++) {
              result <<= 4;
              result |= hexDigits.indexOf(color_str[i][j]);
            }

            uint8_t red = (result >> 16) &  0xFF;
            uint8_t green = (result >> 8) & 0xFF;
            uint8_t blue = (result >> 0) &  0xFF;
            pixels.setPixelColor(i, pixels.Color(red, green, blue));

        }
        digitalWrite(13, color_str[0] == "FFFFFF");
        Serial.println(color_str[0]);
        flag = 0;
        pixels.show();
    }
    
}
