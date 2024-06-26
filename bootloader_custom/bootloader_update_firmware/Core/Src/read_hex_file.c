/**
 * @file        read_hex_file.c
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Includes ----------------------------------------------------------- */
#include "read_hex_file.h"
/* Private defines ---------------------------------------------------- */
#define OFFSET_TO_APP_UPDATE_ADD 0x20000
/* Public variables --------------------------------------------------- */
int internal_buffer_data[50];
uint32_t jump_address = 0;
uint8_t get_address_jump_state = 0;
uint8_t g_flag_write_hex_done = 0;
static hex_form_data hex_struct;
static uint8_t u8calchecksum = 0U;
static uint8_t flag = 0;
static uint32_t app_upd_addr = 0;

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
status_read_hex_file read_all_line(char *pBufferData, uint8_t leng)
{
  field_hex_file state;
  int count = 0U;
  int data_count = 0U;
  void (*ptr)(uint32_t, uint8_t *, uint16_t);
  ptr = flash_write_array;

  for (data_count = 0U; data_count < 16U; data_count++)
  {
    hex_struct.u8Data[data_count] = 0U;
  }
  state = START_CODE;
  for (count = 0; count < leng; count++)
  {
    switch (state)
    {
    case START_CODE:
    {
      if (pBufferData[count] != ':')
      {
        return READ_FAILLED;
      }
      else
      {
        state = BYTE_COUNT;
      }
      break;
    }
    case BYTE_COUNT:
    {
      convert_string_to_hex(&pBufferData[count], 2U);
      hex_struct.u8ByteCount = internal_buffer_data[0];
      count = 2U;
      state = ADDRESS;
      break;
    }
    case ADDRESS:
    {
      convert_string_to_hex(&pBufferData[count], 4U);
      hex_struct.u8Addr[0] = internal_buffer_data[0];
      hex_struct.u8Addr[1] = internal_buffer_data[1];
      count = 6U;
      state = RECORD_TYPE;
      break;
    }
    case RECORD_TYPE:
    {
      convert_string_to_hex(&pBufferData[count], 2U);
      hex_struct.u8RecordType = internal_buffer_data[0];
      count = 8U;
      state = DATA;
      break;
    }
    case DATA:
    {
      if (hex_struct.u8RecordType == 0x04U)
      {
        convert_string_to_hex(&pBufferData[count], 4U);
        hex_struct.u8Start_Addr[0] = internal_buffer_data[0];
        hex_struct.u8Start_Addr[1] = internal_buffer_data[1];
        app_upd_addr = (hex_struct.u8Start_Addr[0] << 24) | (hex_struct.u8Start_Addr[1] << 16);
        flag = 1;
      }
      convert_string_to_hex(&pBufferData[count], hex_struct.u8ByteCount * 2U);
      for (data_count = 0U; data_count < hex_struct.u8ByteCount; data_count++)
      {
        hex_struct.u8Data[data_count] = internal_buffer_data[data_count];
      }
      if (flag == 1 && hex_struct.u8RecordType == 0x00U)
      {
        app_upd_addr = app_upd_addr & 0xFFFF0000;
        app_upd_addr = app_upd_addr | ((hex_struct.u8Addr[0] << 8) | hex_struct.u8Addr[1]);
        if (get_address_jump_state == GET_ADDRESS_TO_JUMP)
        {
          jump_address = app_upd_addr;
          get_address_jump_state = GET_ADDRESS_DONE;
        }
        ptr(app_upd_addr + OFFSET_TO_APP_UPDATE_ADD, (uint8_t *) &hex_struct.u8Data, hex_struct.u8ByteCount);
      }
      count = 8U + (hex_struct.u8ByteCount * 2U);
      state = CHECKSUM;
      break;
    }
    case CHECKSUM:
    {
      convert_string_to_hex(&pBufferData[count], 2U);
      hex_struct.u8Checksum = internal_buffer_data[0];
      state = DONE;
      break;
    }
    case DONE:
    {
      u8calchecksum =
        hex_struct.u8ByteCount + hex_struct.u8Addr[0] + hex_struct.u8Addr[1] + hex_struct.u8RecordType;
      for (data_count = 0U; data_count < hex_struct.u8ByteCount; data_count++)
      {
        u8calchecksum = u8calchecksum + hex_struct.u8Data[data_count];
      }
      u8calchecksum = ~u8calchecksum + 1U;
      if (u8calchecksum == hex_struct.u8Checksum)
      {
        if (hex_struct.u8RecordType == 0x01U)
        {
          g_flag_write_hex_done = 1;
          flag = 0;
          return READ_SUCCESSFULLY;
        }
      }
      else
      {
        flag = 0;
        return READ_FAILLED;
      }
      break;
    }
    default:
    {
      return READ_FAILLED;
      break;
    }
    }
  }
  return READ_SUCCESSFULLY;
}

/**
 * The function "convert_string_to_hex" converts a string of characters representing hexadecimal values
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
void convert_string_to_hex(char *buff, int u32length)
{
  int count = 0U;
  int count1 = 0U;
  int tempBuffer[100];

  for (count = 0U; count < u32length; count++)
  {
    if (buff[count] >= '0' && buff[count] <= '9')
    {
      tempBuffer[count] = buff[count] - 48;
    }
    else if (buff[count] >= 'A' && buff[count] <= 'F')
    {
      tempBuffer[count] = buff[count] - 65 + 10;
    }
    else
    {
      return;
    }
    if (count % 2 != 0)
    {
      internal_buffer_data[count1] = ((tempBuffer[count - 1] << 4) | (tempBuffer[count]));
      count1++;
    }
  }
}
