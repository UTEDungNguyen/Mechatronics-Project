/**
 * @file        flash.h
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Define to prevent recursive inclusion ------------------------------ */
#ifndef INC_FLASH_H_
#define INC_FLASH_H_

/* Includes ----------------------------------------------------------- */
#include <stdint.h>
#include <string.h>

/* Public defines ----------------------------------------------------- */
/* Base address of the Flash sectors */
#define ADDR_FLASH_SECTOR_0 ((uint32_t) 0x08000000) /* Base @ of Sector 0, 16 Kbytes */
#define ADDR_FLASH_SECTOR_1 ((uint32_t) 0x08004000) /* Base @ of Sector 1, 16 Kbytes */
#define ADDR_FLASH_SECTOR_2 ((uint32_t) 0x08008000) /* Base @ of Sector 2, 16 Kbytes */
#define ADDR_FLASH_SECTOR_3 ((uint32_t) 0x0800C000) /* Base @ of Sector 3, 16 Kbytes */
#define ADDR_FLASH_SECTOR_4 ((uint32_t) 0x08010000) /* Base @ of Sector 4, 64 Kbytes */
#define ADDR_FLASH_SECTOR_5 ((uint32_t) 0x08020000) /* Base @ of Sector 5, 128 Kbytes */
#define ADDR_FLASH_SECTOR_6 ((uint32_t) 0x08040000) /* Base @ of Sector 6, 128 Kbytes */

/* Public enumerate/structure ----------------------------------------- */
#pragma pack(1)
typedef struct
{
  uint8_t no;
  uint8_t ssid[30];
  uint8_t pass[30];
} wifi_info_t;
#pragma pack()

/* Public function prototypes ----------------------------------------- */
/**
 * The function Flash_Erase erases a sector of flash memory.
 *
 * @param address The address parameter is the starting address of the flash memory sector that you
 * want to erase.
 */
void flash_erase(uint32_t flash_start_addr, uint8_t nbsector);

/**
 * The function Flash_Write_Int writes an integer value to a specified address in flash memory.
 *
 * @param address The address parameter is the memory address where the value will be written to. It is
 * of type uint32_t, which means it is an unsigned 32-bit integer. This allows for a larger range of
 * memory addresses to be used.
 * @param value The value parameter is the integer value that you want to write to the specified
 * address in flash memory.
 */
void flash_write_int(uint32_t address, int value);

/**
 * The function Flash_Write_Float writes a float value to a specified address in flash memory.
 *
 * @param address The address parameter is the memory address where the float value will be written to
 * in the flash memory.
 * @param f The parameter "f" is a floating-point number that you want to write to the flash memory.
 */
void flash_write_float(uint32_t address, float f);

/**
 * The function Flash_Write_Array writes an array of bytes to a specified address in flash memory.
 *
 * @param address The starting address in flash memory where the array will be written.
 * @param arr The parameter "arr" is a pointer to an array of uint8_t (unsigned 8-bit integer) values.
 * @param leng The parameter "leng" represents the length of the array that needs to be written to the
 * flash memory.
 */
void flash_write_array(uint32_t address, uint8_t *arr, uint16_t leng);

/**
 * The function "Flash_Write_Struct" writes a structure of type "wifi_info_t" to a specified address in
 * flash memory.
 *
 * @param address The address parameter is the starting address in the flash memory where the data will
 * be written. It is of type uint32_t, which means it is a 32-bit unsigned integer.
 * @param data The "data" parameter is of type "wifi_info_t", which is a user-defined structure that
 * contains information related to WiFi settings or configurations.
 */
void flash_write_struct(uint32_t address, wifi_info_t data);

/**
 * The function Flash_Read_Int reads a 16-bit integer from a specified memory address.
 *
 * @param address The address parameter is of type uint32_t, which means it is an unsigned 32-bit
 * integer. It represents the memory address from which the function will read an integer value.
 *
 * @return The function `Flash_Read_Int` returns an `int` value.
 */
int flash_read_int(uint32_t address);

/**
 * The function Flash_Read_Float reads a float value from a specific memory address.
 *
 * @param address The address parameter is the memory address from which the float value will be read.
 *
 * @return a float value.
 */
float flash_read_float(uint32_t address);

/**
 * The function Flash_Read_Array reads an array of bytes from a specified address in flash memory.
 *
 * @param address The starting address from where the data needs to be read from the flash memory.
 * @param arr A pointer to an array where the read data will be stored.
 * @param leng The parameter "leng" represents the length of the array that needs to be read from the
 * flash memory.
 */
void flash_read_array(uint32_t address, uint8_t *arr, uint16_t leng);

/**
 * The function Flash_Read_Struct reads data from flash memory into a wifi_info_t structure.
 *
 * @param address The address parameter is the starting address in the flash memory from where the data
 * needs to be read. It is of type uint32_t, which means it is a 32-bit unsigned integer. This
 * parameter specifies the memory location from where the data needs to be read.
 * @param data The `data` parameter is a pointer to a `wifi_info_t` structure.
 */
void flash_read_struct(uint32_t address, wifi_info_t *data);

#endif /* INC_FLASH_H_ */
/* End of file -------------------------------------------------------- */