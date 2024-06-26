/**
 * @file        command_uart_bootloader.h
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-17
 *
 */

/* Includes ----------------------------------------------------------- */
#include <command_uart_bootloader.h>

/* Public variables --------------------------------------------------- */
extern UART_HandleTypeDef huart1;
extern int internal_buffer_data[50];
static uint8_t read_array_buffer[10] = { 0 };
static command_frame_t command_struct;

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
status_command_handler_t command_handler(function_pointer_t *handle, char *pBufferData, uint8_t leng)
{
  field_command_handler_t state_command;
  uint8_t count = 0U;
  uint8_t data_frame_int_convert = 0;
  uint16_t crc_calculate = 0;
  uint32_t address_handler = 0;
  state_command = START_FRAME;
  for (count = 0; count < leng + 1; count++)
  {
    switch (state_command)
    {
    case START_FRAME:
    {
      if (pBufferData[count] != '~')
      {
        return COMMAND_FAIL;
      }
      else
      {
        state_command = COMMAND_FRAME;
      }
      break;
    }
    case COMMAND_FRAME:
    {
      handle->ptr_convert_string_to_hex(&pBufferData[count], 2U);
      command_struct.cmd = internal_buffer_data[0];
      count = 2U;
      state_command = ADDRESS_FRAME;
      break;
    }
    case ADDRESS_FRAME:
    {
      handle->ptr_convert_string_to_hex(&pBufferData[count], 8U);
      command_struct.addr[0] = internal_buffer_data[0];
      command_struct.addr[1] = internal_buffer_data[1];
      command_struct.addr[2] = internal_buffer_data[2];
      command_struct.addr[3] = internal_buffer_data[3];
      address_handler = ((command_struct.addr[0] << 24) | (command_struct.addr[1] << 16)
                         | (command_struct.addr[2] << 8) | (command_struct.addr[3]));
      count = 10U;
      state_command = DATA_FRAME;
      break;
    }
    case DATA_FRAME:
    {
      handle->ptr_convert_string_to_hex(&pBufferData[count], 2U);
      command_struct.data = internal_buffer_data[0];
      data_frame_int_convert = (uint8_t) command_struct.data;
      count = 12U;
      state_command = CRC_FRAME;
      break;
    }
    case CRC_FRAME:
    {
      handle->ptr_convert_string_to_hex(&pBufferData[count], 4U);
      command_struct.crc = ((internal_buffer_data[0] << 8) | internal_buffer_data[1]);
      uint8_t frame[] = { 0x7E,
                          command_struct.cmd,
                          command_struct.addr[0],
                          command_struct.addr[1],
                          command_struct.addr[2],
                          command_struct.addr[3],
                          command_struct.data };
      uint8_t frame_length = sizeof(frame) / sizeof(frame[0]);
      crc_calculate = calculateCRC16(frame, frame_length);
      count = 16U;
      state_command = DONE_FRAME;
      break;
    }
    case DONE_FRAME:
    {
      if (command_struct.crc == crc_calculate)
      {
        switch (command_struct.cmd)
        {
        case WRITE_COMMAND:
          handle->ptr_hal_uart_transmit(&huart1, (uint8_t *) "Ready write hex command", 23);
          return WRITE_COMMAND;
          break;
        case READ_COMMAND:
          handle->ptr_read_array(address_handler, read_array_buffer, (uint16_t) data_frame_int_convert);
          handle->ptr_hal_uart_transmit(&huart1, (uint8_t *) "Read command successfull", 24);
          return READ_COMMAND;
          break;
        case ERASE_COMMAND:
          handle->ptr_erase_flash(address_handler, data_frame_int_convert);
          handle->ptr_hal_uart_transmit(&huart1, (uint8_t *) "Erase command successfull", 25);
          return ERASE_COMMAND;
          break;
        case JUMP_TO_ADDRESS_COMMAND:
          handle->ptr_hal_uart_transmit(&huart1, (uint8_t *) "Jump successfull", 16);
          handle->ptr_delay(2);
          handle->ptr_bootloader_jump_to_address(address_handler);
          return JUMP_TO_ADDRESS_COMMAND;
          break;
        default: break;
        }
      }
      else
      {
        return COMMAND_FAIL;
      }
      break;
    }
    default:
    {
      return COMMAND_FAIL;
      break;
    }
    }
  }
  return COMMAND_FAIL;
}

// Function to calculate CRC-16 value
/**
 * The function calculates a 16-bit CRC (Cyclic Redundancy Check) value for a given data array.
 *
 * @param data A pointer to an array of uint8_t data that needs to be checked for CRC.
 * @param length The "length" parameter represents the length of the data array, which is the number of
 * elements in the array.
 *
 * @return a uint16_t value, which is the final calculated CRC16 value.
 */
uint16_t calculateCRC16(const uint8_t *data, uint8_t length)
{
  uint16_t crc = 0xFFFF;  // Initial value

  for (uint8_t i = 0; i < length; i++)
  {
    crc ^= (uint16_t) data[i];

    for (int j = 0; j < 8; j++)
    {
      if (crc & 0x0001)
      {
        crc = (crc >> 1) ^ CRC16_POLYNOMIAL;
      }
      else
      {
        crc >>= 1;
      }
    }
  }

  return crc;  // Final value
}
