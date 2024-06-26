/**
 * @file        command_uart_bootloader.c
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-17
 *
 */

/* Define to prevent recursive inclusion ------------------------------ */
#ifndef INC_COMMAND_UART_BOOTLOADER_H_
#define INC_COMMAND_UART_BOOTLOADER_H_

/* Public defines ----------------------------------------------------- */
// Polynomial for CRC-16 (0x8005)
#define CRC16_POLYNOMIAL 0x8005

/* Includes ----------------------------------------------------------- */
#include "read_hex_file.h"

/* Public enumerate/structure ----------------------------------------- */
typedef struct function_poiniter_s
{
  void (*ptr_delay)(uint32_t);
  HAL_StatusTypeDef (*ptr_hal_uart_transmit)(UART_HandleTypeDef *, uint8_t *, uint16_t);
  void (*ptr_convert_string_to_hex)(char *, int);
  void (*ptr_erase_flash)(uint32_t, uint8_t);
  void (*ptr_bootloader_jump_to_address)(uint32_t);
  void (*ptr_read_array)(uint32_t, uint8_t *, uint16_t);
} function_pointer_t;

typedef struct
{
  uint8_t cmd;
  uint8_t addr[4];
  uint8_t data;
  uint16_t crc;
} command_frame_t;

typedef enum
{
  COMMAND_FAIL = 0x31,
  WRITE_COMMAND = 0x01,
  READ_COMMAND = 0x02,
  ERASE_COMMAND = 0x03,
  JUMP_TO_ADDRESS_COMMAND = 0x04
} status_command_handler_t;

typedef enum
{
  START_FRAME = 0U,
  COMMAND_FRAME = 1U,
  ADDRESS_FRAME = 2U,
  DATA_FRAME = 3U,
  CRC_FRAME = 4U,
  DONE_FRAME = 5U
} field_command_handler_t;

/* Public function prototypes ----------------------------------------- */

/**
 * The function `command_handler` processes a command frame received over UART and performs different
 * actions based on the command type.
 *
 * @param handle A pointer to a structure or object that contains function pointers for various
 * operations.
 * @param pBufferData A pointer to a buffer containing the received data.
 * @param leng The parameter "leng" represents the length of the input buffer data, which is the number
 * of characters in the "pBufferData" array.
 *
 * @return a status_command_handler_t value.
 */
status_command_handler_t command_handler(function_pointer_t *handle, char *pBufferData, uint8_t leng);

/* Private function prototypes ----------------------------------------- */
/**
 * The function calculates a 16-bit CRC (Cyclic Redundancy Check) value for a given data array.
 *
 * @param data A pointer to an array of uint8_t data that needs to be checked for CRC.
 * @param length The "length" parameter represents the length of the data array, which is the number of
 * elements in the array.
 *
 * @return a uint16_t value, which is the final calculated CRC16 value.
 */
uint16_t calculateCRC16(const uint8_t *data, uint8_t length);

#endif /* INC_COMMAND_UART_BOOTLOADER_H_ */
