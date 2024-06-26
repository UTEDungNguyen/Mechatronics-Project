/**
 * @file        read_hex_file.h
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Define to prevent recursive inclusion ------------------------------ */
#ifndef INC_READ_HEX_FILE_H_
#define INC_READ_HEX_FILE_H_

/* Includes ----------------------------------------------------------- */
#include "bootloader.h"
#include "flash.h"

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Public enumerate/structure ----------------------------------------- */
typedef enum
{
  START_CODE = 0U,
  BYTE_COUNT = 1U,
  ADDRESS = 2U,
  RECORD_TYPE = 3U,
  DATA = 4U,
  CHECKSUM = 5U,
  DONE = 6U
} field_hex_file;

typedef enum
{
  READ_SUCCESSFULLY = 0U,
  READ_FAILLED
} status_read_hex_file;

typedef struct
{
  uint8_t u8ByteCount;
  uint8_t u8Addr[2];
  uint8_t u8Start_Addr[2];
  uint8_t u8RecordType;
  uint8_t u8Data[16];
  uint8_t u8Checksum;
} hex_form_data;

typedef enum
{
  GET_ADDRESS_TO_JUMP,
  GET_ADDRESS_DONE
} get_address_to_jump_t;

/* Public function prototypes ----------------------------------------- */
/**
 * The function ReadAllLine reads a hex file line by line and converts the data into a structured
 * format.
 *
 * @param pBufferData A pointer to a buffer containing the data to be read.
 * @param leng The parameter "leng" represents the length of the buffer data that is being passed to
 * the function.
 *
 * @return a value of type "StatusReadHexFile".
 */
status_read_hex_file read_all_line(char *pBufferData, uint8_t leng);

/* Private function prototypes ----------------------------------------- */
/**
 * The function "ConvertStringtoHex" converts a string of characters representing hexadecimal values
 * into an array of corresponding hexadecimal values.
 *
 * @param buff A pointer to a character array that contains the string to be converted to hexadecimal.
 * @param u32length The parameter `u32length` represents the length of the input string `buff`. It is
 * an integer value that specifies the number of characters in the string that needs to be converted to
 * hexadecimal.
 *
 * @return The function does not explicitly return a value. However, if the condition in the else
 * statement is met, the function will exit and no further code will be executed.
 */
void convert_string_to_hex(char *buff, int u32length);

#endif /* INC_READ_HEX_FILE_H_ */
