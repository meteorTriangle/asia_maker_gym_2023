#include <Servo.h>
//const uint8_t LED_pin[3] = {9, 10, 11};
//uint32_t color_code = 0xED0CC8;


//{Horizon servo pin, vertical servo pin}
const uint8_t Servo_pin[3][2] = {{2, 3}, {4, 5}, {6, 7}};
uint16_t Servo_deg[3][2] = {{90, 90}, {90, 90}, {90, 90}};
Servo myservo[3][2];


void setup()
{
    for(int i = 0; i< 3; i++){
        for(int j = 0; j < 2; j++){
            myservo[i][j].attach(Servo_pin[i][j]);
        }
    }
    Serial.begin(115200);
    Serial.setTimeout(10);

    //initial servo
    for(int i = 0; i < 3; i++){
        myservo[i][0].write(90);//horizon
    }
    for(int i = 0; i < 3; i++){
        myservo[i][1].write(90);//vertical
    }
    /*  ////LED
    for(int i = 0; i < 3; i++){
        pinMode(LED_pin[i], OUTPUT);
    }
    */
}

bool flag = 0;
String data;
void loop()
{
    
    if(Serial.available()){
        data = Serial.readStringUntil('M'); ///Serial.readString()
        flag = 1;
    }
    if(flag){
        //Serial.println(data);
        bool flag = 0;
        int nn = data.indexOf('m');
        String data__ = data.substring(nn+1);
        for(int i = 0; i < 3; i++){
            for(int j = 0; j < 2; j++){
                String degT = data__.substring(((i*2)+j)*5, (((i*2)+j)*5)+4); //(((i*2)+j)*4)+3
                Servo_deg[i][j] = degT.toInt();
                myservo[i][j].writeMicroseconds(Servo_deg[i][j]);
                //Serial.print(String(Servo_deg[i][j]) + ' ');
            }
        }
        //Serial.println(' ');
    
    flag = 0;
    }
///12m123 132 012 045 120 110M

    /*    ////LED
    for(int i = 0; i < 3; i++){
        analogWrite(LED_pin[i], 255-((color_code>>(8*i))&0xFF));
    }
	*/
}
