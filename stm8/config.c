#include "config.h"
#include "eeprom.h"

#include <string.h>

#define SYSTEM_CONFIG ((cfg_system_t *)0x4000)
#define OUTPUT_CONFIG ((cfg_output_t *)0x4040)

void validate_system_config(cfg_system_t *sys)
{
	if (sys->name[0] == 0) {
		strcpy(sys->name, "Unnamed");
		sys->default_on = 0;
		sys->autocommit = 1;
	}

	if (sys->vin_adc.a == 0) {
		sys->vin_adc.a = 16 << 10;
		sys->vin_adc.b = 0;
	}

	if (sys->vout_adc.a == 0) {
		sys->vout_adc.a = 14027; // 1/0.073 << 10
		sys->vout_adc.b = 462; // (452<<10) / 1000; giving constant here since it can overflow in uint16_t
	}

	if (sys->cout_adc.a == 0) {
		sys->cout_adc.a = 1280; //(125<<10)/100; giving constant here since it can overflow in uint16_t
		sys->cout_adc.b = (2<<10)/10;
	}

	if (sys->vout_pwm.a == 0) {
		sys->vout_pwm.a = 75; // 0.073 = (73<<10)/1000
		sys->vout_pwm.b = 34; // 0.033 = (33<<10)/1000
	}

	if (sys->cout_pwm.a == 0) {
		sys->cout_pwm.a = 819; // 0.8 = (8<<10)/10
		sys->cout_pwm.b = 164; // 0.160 = (16<<10)/100
	}
}

void config_load_system(cfg_system_t *sys)
{
	memcpy(sys, SYSTEM_CONFIG, sizeof(*sys));
	validate_system_config(sys);
}

void config_save_system(cfg_system_t *sys)
{
	eeprom_save_data((uint8_t*)SYSTEM_CONFIG, (uint8_t*)sys, sizeof(*sys));
}

void validate_output_config(cfg_output_t *cfg)
{
	if (cfg->vset == 0 || cfg->cset == 0) {
		cfg->output = 0;
		cfg->vset = 5<<10; // 5V
		cfg->cset = (1<<10) / 2; // 0.5A
		cfg->vshutdown = 0;
		cfg->cshutdown = 0;
	}
}

void config_load_output(cfg_output_t *cfg)
{
	memcpy(cfg, OUTPUT_CONFIG, sizeof(*cfg));
	validate_output_config(cfg);
}

void config_save_output(cfg_output_t *cfg)
{
	eeprom_save_data((uint8_t*)OUTPUT_CONFIG, (uint8_t*)cfg, sizeof(*cfg));
}