#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/i2c.h"
#include "hardware/timer.h"
#include "hardware/pwm.h"
//#include "hardware/clocks.h"



// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments
#define I2C_PORT i2c1
#define I2C_SDA 14
#define I2C_SCL 15

/// @brief LED_on command
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
    set_sys_clock_khz(125000, true);
    stdio_init_all();
    uint64_t ref_time = time_us_64();
    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 400*1000);
    gpio_set_function(I2C_SDA, GPIO_FUNC_I2C);
    gpio_set_function(I2C_SCL, GPIO_FUNC_I2C);
    gpio_pull_up(I2C_SDA);
    gpio_pull_up(I2C_SCL);
    //servo pwm initial
    gpio_set_function(0, GPIO_FUNC_PWM);
    pwm_config servo_pwm_config =  pwm_get_default_config();
    pwm_config_set_clkdiv_int(&servo_pwm_config, 250);
    pwm_config_set_wrap(&servo_pwm_config, 10000);
    uint slice_num = pwm_gpio_to_slice_num(0);
    pwm_init(slice_num, &servo_pwm_config, false);
    pwm_set_enabled(slice_num, true); 
    pwm_set_chan_level(slice_num, PWM_CHAN_A, 5000);

    sleep_ms(3000);
    
    //check connection status
    bool spotlight_status[12];
    check_connection(&spotlight_status[0]); 

    gpio_init(25);
    gpio_set_dir(25, true);

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
            if(receieve_data[1] == 0x06){          // 0x06 <servo_H_bit> <servo_L_bit> elevator
                int elevator_servo_us = (int(receieve_data[2])<<8) | int(receieve_data[3]);
                printf("%d", elevator_servo_us);
                pwm_set_chan_level(slice_num, PWM_CHAN_A, elevator_servo_us/2);
            }
        }
    }


    return 0;
}