#include <Servo.h>
#include <Wire.h>
#include <EEPROM.h>

///pin define  
#define pin_Servo_Horizon 7
#define pin_Servo_Vertical 8
#define pin_redLed 3
#define pin_greenLed 5
#define pin_blueLed 6

///EEPROM address define  
#define I2C_address_EE 0x01
#define ServoAdj_Horizon_H_EE 0x02
#define ServoAdj_Horizon_L_EE 0x03
#define ServoAdj_Vertical_H_EE 0x04
#define ServoAdj_Vertical_L_EE 0x05

Servo Servo_H, Servo_L;

void setup(){
    Serial.begin(1000000);
    EEPROM.begin();
    uint8_t I2C_address = EEPROM.read(I2C_address_EE);
    if(I2C_address == 0xFF){
        I2C_address = 0x55;
    }
    Wire.begin(I2C_address);
    Servo_H.attach(pin_Servo_Horizon);
    Servo_L.attach(pin_Servo_Vertical);
    pinMode(pin_redLed, OUTPUT);
    pinMode(pin_greenLed, OUTPUT);
    pinMode(pin_blueLed, OUTPUT);
}
bool Serial_flag = 0;
String Serial_data = "";
void loop(){
    if(Serial.available()){
        Serial_data = Serial.readStringUntil('M');
        Serial_flag = 1;
    }
    if(Serial_flag){
        String command = Serial_data.substring(0, 2);
        if(command == "02"){                  //02  I2C address set // format "02 <address>" //ex "02 01"
            String I2C_address_str = Serial_data.substring(3, 5);
            uint8_t I2C_address = I2C_address_str.toInt();
            EEPROM.write(I2C_address_EE, I2C_address);
            Wire.end();
            Wire.begin(I2C_address);
        }
        if(command == "03"){                  //03 I2C address get // format "03" //ex "03"
            uint8_t I2C_address = EEPROM.read(I2C_address_EE);
            Serial.print(String(I2C_address) + "M");
        }

        Serial_flag = 0;
    }
    
}