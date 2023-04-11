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

Servo Servo_H, Servo_V;

uint16_t ServoAdj_Horizon, ServoAdj_Vertical;

void setup(){
    Serial.begin(1000000);
    EEPROM.begin();
    uint8_t I2C_address = EEPROM.read(I2C_address_EE);
    if(I2C_address == 0xFF){
        I2C_address = 0x55;
    }
    ServoAdj_Horizon = ((uint16_t)EEPROM.read(ServoAdj_Horizon_H_EE) << 8) | (uint16_t)EEPROM.read(ServoAdj_Horizon_L_EE);
    ServoAdj_Vertical = ((uint16_t)EEPROM.read(ServoAdj_Vertical_H_EE) << 8) | (uint16_t)EEPROM.read(ServoAdj_Vertical_L_EE);
    Wire.begin(I2C_address);
    Servo_H.attach(pin_Servo_Horizon);
    Servo_V.attach(pin_Servo_Vertical);
    pinMode(pin_redLed, OUTPUT);
    pinMode(pin_greenLed, OUTPUT);
    pinMode(pin_blueLed, OUTPUT);
    Wire.onReceive(I2C_receieve);
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
            char c[2];
            sprintf(c, "%02d", I2C_address);
            Serial.print(String(c) + "M");
        }
        if(command == "04"){                  //04 adj Servo horizontal // format "04" //ex "04"
            ServoAdj_Horizon = Servo_H.readMicroseconds();
            uint8_t ServoAdj_Horizon_H = (ServoAdj_Horizon >> 8) & 0xFF;
            uint8_t ServoAdj_Horizon_L = (ServoAdj_Horizon) & 0xFF;
            EEPROM.write(ServoAdj_Horizon_H_EE, ServoAdj_Horizon_H);
            EEPROM.write(ServoAdj_Horizon_L_EE, ServoAdj_Horizon_L);
            //Serial.print(ServoAdj_Horizon_H*(int)256 + ServoAdj_Horizon_L);
        }
        if(command == "05"){                  //05 adj Servo vertical // format "05" //ex "05"
            ServoAdj_Vertical = Servo_V.readMicroseconds();
            uint8_t ServoAdj_Vertical_H = (ServoAdj_Vertical >> 8) & 0xFF;
            uint8_t ServoAdj_Vertical_L = (ServoAdj_Vertical) & 0xFF;
            EEPROM.write(ServoAdj_Vertical_H_EE, ServoAdj_Vertical_H);
            EEPROM.write(ServoAdj_Vertical_L_EE, ServoAdj_Vertical_L);
            //Serial.print(ServoAdj_Vertical_H*(int)256 + ServoAdj_Vertical_L);
        }
        if(command == "06"){                  //06 set Servo // format "06 <Horizontal servo> <Vertical servo>" //ex "06 0500 1200"
            int Servo_Horizon_us = Serial_data.substring(3, 7).toInt();
            int Servo_Vertical_us = Serial_data.substring(8, 12).toInt();
            servo__set(Servo_Horizon_us, Servo_Vertical_us);
        }
        if(command == "07"){                  //07 set LED // format "07 <Red> <Green> <Blue>" //ex "07 233 210 033"
            int LED_red = Serial_data.substring(3, 6).toInt();
            int LED_green = Serial_data.substring(7, 10).toInt();
            int LED_blue = Serial_data.substring(11, 14).toInt();
            analogWrite(pin_redLed,   255 - LED_red);
            analogWrite(pin_greenLed, 255 - LED_green);
            analogWrite(pin_blueLed,  255 - LED_blue);
        }
        Serial_flag = 0;
    }
    
}

void I2C_receieve(int bytes_Q){
    uint8_t I2C_read[bytes_Q];
    Wire.readBytes(I2C_read, bytes_Q);
    if(I2C_read[0] == 8){  //[8] [<Servo_Horizon_H>] [<Servo_Horizon_L>] [<Servo_Vertical_H>] [<Servo_Vertical_L>]
        int Servo_Horizon_H = I2C_read[1];
        int Servo_Horizon_L = I2C_read[2];
        int Servo_Vertical_H = I2C_read[3];
        int Servo_Vertical_L = I2C_read[4];
        int Servo_Horizon_us = (Servo_Horizon_H << 8) | Servo_Horizon_L;
        int Servo_Vertical_us = (Servo_Vertical_H << 8) | Servo_Vertical_L;
        servo__set(Servo_Horizon_us, Servo_Vertical_us);
    }
    if(I2C_read[0] == 9){  //[9] [<Red>] [<Green>] [<Blue>]
        uint8_t LED_red = I2C_read[1];
        uint8_t LED_green = I2C_read[2];
        uint8_t LED_blue  = I2C_read[3];
        analogWrite(pin_redLed,   255 - LED_red);
        analogWrite(pin_greenLed, 255 - LED_green);
        analogWrite(pin_blueLed,  255 - LED_blue);
    }
}

void servo__set(int H, int V){
    int adj_H = ServoAdj_Horizon - 1500;
    int adj_V = ServoAdj_Vertical - 1500;
    Servo_H.writeMicroseconds(H + adj_H);
    Servo_V.writeMicroseconds(V + adj_V);
}
