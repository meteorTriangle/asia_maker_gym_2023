#include <stdio.h>
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

const uint8_t addr_1_off[] = {0x09, 0xFF, 0xFF, 0xFF};
const uint8_t addr_1_on[] = {0x09, 0x00, 0x00, 0x00};

/// @brief check every spotlight nano is connected
/// @param status 
void check_connection(bool *status){
    for(int addr_=0; addr_<12; addr_++){
        int error = i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_off[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
        *status++ = error > 0;
    }
    sleep_ms(1000);
    for(int addr_=0; addr_<12; addr_++){
        if(status[addr_]){
            i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_on[0], sizeof(addr_1_on)/sizeof(addr_1_on[0]), false, 1000);
        }
    }
    sleep_ms(1000);
    for(int addr_=0; addr_<12; addr_++){
        if(status[addr_]){
            i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_off[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
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
    
    // I2C Initialisation. Using it at 400Khz.
    i2c_init(I2C_PORT, 100*1000);
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


    while(true){
        for(int addr_=0; addr_<12; addr_++){
            if(spotlight_status[addr_]){
                i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_on[0], sizeof(addr_1_on)/sizeof(addr_1_on[0]), false, 1000);
                sleep_ms(500);
                i2c_write_timeout_us(I2C_PORT, addr_, &addr_1_off[0], sizeof(addr_1_off)/sizeof(addr_1_off[0]), false, 1000);
            }
        }
    }


    return 0;
}

