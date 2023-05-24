#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "hardware/timer.h"
//#include "hardware/clocks.h"



// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define I2C_PORT i2c1
#define I2C_SDA 14
#define I2C_SCL 15

const uint8_t addr_1_on[] = {0x09, 0xFF, 0xFF, 0xFF};
const uint8_t addr_1_off[] = {0x09, 0x00, 0x00, 0x00};

/// @brief check every spotlight nano is connected
/// @param status 
void check_connection(bool *status){
    for(int addr_=0; addr_<12; addr_++){
        int error = i2c_write_timeout_us(I2C_PORT, addr_+1, &addr_1_on[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
        *(status+addr_) = error > 0;
    }
    sleep_ms(1000);
    for(int addr_=0; addr_<12; addr_++){
        if(*(status+addr_)){
            i2c_write_timeout_us(I2C_PORT, addr_+1, &addr_1_off[0], sizeof(addr_1_on)/sizeof(addr_1_on[0]), false, 1000);
        }
    }
    sleep_ms(1000);
    for(int addr_=0; addr_<12; addr_++){
        if(*(status+addr_)){
            i2c_write_timeout_us(I2C_PORT, addr_+1, &addr_1_on[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
            sleep_ms(500);
        }
    }
    
}

/*
int64_t alarm_callback(alarm_id_t id, void *user_data) {
    // Put your timeout handler code in here
    return 0;
}
*/


int main()
{
    stdio_init_all();
    uint64_t ref_time = time_us_64();
    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);
    sleep_ms(3000);
    
    //check connection status
    bool spotlight_status[12];
    check_connection(&spotlight_status[0]);
    printf("status: ");
    for(int ii=0; ii<12; ii++){
        printf("%s  ", spotlight_status[ii] ? "0" : "*");
    }
    printf("\n");

    // Timer example code - This example fires off the callback after 2000ms
    //add_alarm_in_ms(2000, alarm_callback, NULL, false);
    gpio_init(25);
    gpio_set_dir(25, true);
    //stdio_set_chars_available_callback();
    /*
    for(uint16_t servo_v_=1500; servo_v_<2300; servo_v_+=20){
        uint8_t servo_act[5] = {0x08, uint8_t(servo_v_>>8), (uint8_t)servo_v_, uint8_t(servo_v_>>8), (uint8_t)servo_v_};
        for(int addr_=1; addr_<13; addr_++){
            if(spotlight_status[addr_ - 1]){
                i2c_write_timeout_us(I2C_PORT, addr_, &servo_act[0], sizeof(servo_act)/sizeof(servo_act[0]), false, 1000);
            }
        }
        sleep_ms(10);
    }
    */

    uint8_t receieve_data[100];
    bool last_receieve_status = false;
    bool receieve_status = false;
    bool flag = false;
    while(true){
        int receieve_ = getchar_timeout_us(1);
        receieve_status = receieve_ != -1;
        if(receieve_status && (!last_receieve_status)){
            receieve_data[0] = 0;
        }
        if(receieve_status){
            receieve_data[0]++;
            receieve_data[receieve_data[0]] = receieve_;
        }
        if(!receieve_status && last_receieve_status){
            flag = true;
        }
        last_receieve_status = receieve_status;

        if(flag){
            ref_time = time_us_64();
            for(uint8_t i = 1; i <= receieve_data[0]; i++){
                printf("%d-", receieve_data[i]);
            }
            printf("\n");
            flag = false;
            if(receieve_data[1] == 0x01){      //0x01 <addr> <red> <green> <blue>         set spotlight color
                uint8_t transData[4] = {0x09, receieve_data[3], receieve_data[4], receieve_data[5]};
                uint8_t addr = receieve_data[2];
                if(spotlight_status[addr - 1]){
                    i2c_write_timeout_us(I2C_PORT, addr, &transData[0], sizeof(transData)/sizeof(transData[0]), false, 400);
                    printf("set\n");
                }
            }
            if(receieve_data[1] == 0x02){         // status
                for(int ii=0; ii<12; ii++){
                    printf("%s  ", spotlight_status[ii] ? "0" : "*");
                }
            }
            if(receieve_data[1] == 0x03){         //0x03 <addr> <servoHor_H> <servoHor_L> <servoVer_H> <servoVer_L>
                uint8_t transData[5] = {0x08, receieve_data[3], receieve_data[4], receieve_data[5], receieve_data[6]};
                uint8_t addr = receieve_data[2];
                if(spotlight_status[addr - 1]){
                    i2c_write_timeout_us(I2C_PORT, addr, &transData[0], sizeof(transData)/sizeof(transData[0]), false, 400);
                    printf("set\n");
                }
            }
            if(receieve_data[1] == 0x04){        //0x04 <servo1_H_h> <servo1_H_l> <servo1_V_h> <servo1_V_l> <servo2_H_h> <servo2_H_l> <servo2_V_h> <servo2_V_l>.............
                for(int i = 0; i< 9; i++){
                    uint8_t transData[5] = {0x08, receieve_data[2+(4*i)], receieve_data[3+(4*i)], receieve_data[4+(4*i)], receieve_data[5+(4*i)]};
                    if(spotlight_status[i]){
                        i2c_write_timeout_us(I2C_PORT, i+1, &transData[0], sizeof(transData)/sizeof(transData[0]), false, 400);
                    }
                }
            }
            if(receieve_data[1] == 0x05){        //0x05 <r1> <g1> <b1> <r2> <g2> <b2>
                for(int i = 0; i< 9; i++){
                    uint8_t transData[5] = {0x09, receieve_data[2+(3*i)], receieve_data[3+(3*i)], receieve_data[4+(3*i)]};
                    if(spotlight_status[i]){
                        i2c_write_timeout_us(I2C_PORT, i+1, &transData[0], sizeof(transData)/sizeof(transData[0]), false, 400);
                    }
                }
            }
            //printf("%lu\n", (long)(time_us_64()-ref_time));
        }
        /*
        for(uint16_t servo_v_=2300; servo_v_>600; servo_v_-=20){
            uint8_t servo_act[5] = {0x08, uint8_t(servo_v_>>8), (uint8_t)servo_v_, uint8_t(servo_v_>>8), (uint8_t)servo_v_};
            for(int addr_=1; addr_<13; addr_++){
                if(spotlight_status[addr_ - 1]){
                    i2c_write_timeout_us(I2C_PORT, addr_, &servo_act[0], sizeof(servo_act)/sizeof(servo_act[0]), false, 1000);
                }
            }
            if(time_us_64() - ref_time > 2000*1000){
                for(int addr_=1; addr_<13; addr_++){
                    if(spotlight_status[addr_ - 1]){
                        uint8_t LED__[] = {0x09, (uint8_t)(rand()%256), (uint8_t)(rand()%256), (uint8_t)(rand()%256)}; 
                        i2c_write_timeout_us(I2C_PORT, addr_, &LED__[0], sizeof(LED__)/sizeof(LED__[0]), false, 1000);
                    }
                }
                ref_time = time_us_64();
            }
            sleep_ms(10);
        }
        
        for(uint16_t servo_v_=600; servo_v_<2300; servo_v_+=20){
            uint8_t servo_act[5] = {0x08, uint8_t(servo_v_>>8), (uint8_t)servo_v_, uint8_t(servo_v_>>8), (uint8_t)servo_v_};
            for(int addr_=1; addr_<13; addr_++){
                if(spotlight_status[addr_ - 1]){
                    i2c_write_timeout_us(I2C_PORT, addr_, &servo_act[0], sizeof(servo_act)/sizeof(servo_act[0]), false, 1000);
                    
                }
            }
            if(time_us_64() - ref_time > 2000*1000){
                for(int addr_=1; addr_<13; addr_++){
                    if(spotlight_status[addr_ - 1]){
                        uint8_t LED__[] = {0x09, (uint8_t)(rand()%256), (uint8_t)(rand()%256), (uint8_t)(rand()%256)}; 
                        i2c_write_timeout_us(I2C_PORT, addr_, &LED__[0], sizeof(LED__)/sizeof(LED__[0]), false, 1000);
                    }
                }
                ref_time = time_us_64();
            }
            sleep_ms(10);
        }
        */
        /*
        for(int addr_=1; addr_<13; addr_++){
            if(spotlight_status[addr_ - 1]){
                i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_off[0], sizeof(addr_1_on)/sizeof(addr_1_on[0]), false, 1000);
                sleep_ms(80);
                i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_on[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
                sleep_ms(80);
            }
        }*/
    }


    return 0;
}

