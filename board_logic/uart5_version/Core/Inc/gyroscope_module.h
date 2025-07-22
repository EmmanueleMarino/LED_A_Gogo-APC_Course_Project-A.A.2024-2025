/* Header file for a "software module" developed to
 * encapsulate code and definitions relative to the
 * "L3GD20" gyroscope which is mounted on the
 * "STM32F3DISCOVERY" board and communicates
 * with the SoC via an SPI interface.
 */

#ifndef GYROSCOPE_MODULE_H
#define GYROSCOPE_MODULE_H

/* /------------------------------\
 *| GYROSCOPE REGISTER DEFINITIONS |					// Refer to pag.29 of the "L3GD20" Reference Manual
 * \------------------------------/
 * Each label corresponds to the hexadecimal
 * value of the respective register's address */

// [COUPLES OF 8-BIT OUTPUT REGISTERS FOR EACH AXIS]
#define GYROSCOPE_OUTPUT_REGISTER_X_LSB 0x28	// OUT_X_L
#define GYROSCOPE_OUTPUT_REGISTER_X_MSB 0x29	// OUT_X_H
#define GYROSCOPE_OUTPUT_REGISTER_Y_LSB 0x2A	// OUT_Y_L
#define GYROSCOPE_OUTPUT_REGISTER_Y_MSB 0x2B	// OUT_Y_H
#define GYROSCOPE_OUTPUT_REGISTER_Z_LSB 0x2C	// OUT_Z_L
#define GYROSCOPE_OUTPUT_REGISTER_Z_MSB 0x2D	// OUT_Z_H

// [CONTROL REGISTERS]
#define GYROSCOPE_CONTROL_REGISTER_1 0x20H		// CTRL_REG1
#define GYROSCOPE_CONTROL_REGISTER_2 0x21H		// CTRL_REG2
#define GYROSCOPE_CONTROL_REGISTER_3 0x22H		// CTRL_REG3
#define GYROSCOPE_CONTROL_REGISTER_4 0x23H		// CTRL_REG4
#define GYROSCOPE_CONTROL_REGISTER_5 0x24H		// CTRL_REG5

// [STATUS REGISTER] -> to check on "overrun"
// errors or new data availability on each axis
#define GYROSCOPE_STATUS_REGISTER 0x27H			// STATUS_REG

/* /------------------------------------------------------------\
 *| ANGULAR VELOCITY MEASURED ON THE THREE AXIS OF THE GYROSCOPE |
 * \------------------------------------------------------------/*/
typedef struct {
	/*  /------------------------------------------------------\
	 * | The "L3GD20" outputs the measured angular velocity on  |
	 * | six 8-bits registers (two registers for each axis:     |
	 * | one register which holds the least significant byte    |
	 * | (E.G. "OUT_X_L"), one which holds the most significant |
	 * | byte(E.G. "OUT_X_H")                                   |
	 *  \------------------------------------------------------/ */
	int16_t x;	// OUT_X_H + OUT_X_L
	int16_t y;	// OUT_Y_H + OUT_Y_L
	int16_t z;	// OUT_Z_H + OUT_Z_L
	// These measurements are signed integers ("two's complement" representation)
} angular_velocity;

#endif
