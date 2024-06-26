/**
 * @file        flash.c
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Includes ----------------------------------------------------------- */
#include <flash.h>
#include <stm32f4xx.h>
/* Private defines ---------------------------------------------------- */
/* Private enumerate/structure ---------------------------------------- */
/* Private macros ----------------------------------------------------- */
/* Public variables --------------------------------------------------- */
/* Private variables -------------------------------------------------- */
/* Private function prototypes ---------------------------------------- */
/* Function definitions ----------------------------------------------- */
/**
 * @brief Gets the sector of a given address
 * @param None
 * @retval The sector of a given address
 */
uint32_t get_sector(uint32_t address)
{
  uint32_t sector = 0;

  if ((address < ADDR_FLASH_SECTOR_1) && (address >= ADDR_FLASH_SECTOR_0))
  {
    sector = FLASH_SECTOR_0;
  }
  else if ((address < ADDR_FLASH_SECTOR_2) && (address >= ADDR_FLASH_SECTOR_1))
  {
    sector = FLASH_SECTOR_1;
  }
  else if ((address < ADDR_FLASH_SECTOR_3) && (address >= ADDR_FLASH_SECTOR_2))
  {
    sector = FLASH_SECTOR_2;
  }
  else if ((address < ADDR_FLASH_SECTOR_4) && (address >= ADDR_FLASH_SECTOR_3))
  {
    sector = FLASH_SECTOR_3;
  }
  else if ((address < ADDR_FLASH_SECTOR_5) && (address >= ADDR_FLASH_SECTOR_4))
  {
    sector = FLASH_SECTOR_4;
  }
  else if ((address < ADDR_FLASH_SECTOR_6) && (address >= ADDR_FLASH_SECTOR_5))
  {
    sector = FLASH_SECTOR_5;
  }
  else if (address >= ADDR_FLASH_SECTOR_6)
  {
    sector = FLASH_SECTOR_6;
  }
  return sector;
}

/**
 * The function Flash_Erase erases a sector of flash memory.
 *
 * @param address The address parameter is the starting address of the flash memory sector that you
 * want to erase.
 */
void flash_erase(uint32_t flash_start_addr, uint8_t nbsector)
{
  HAL_FLASH_Unlock();
  FLASH_EraseInitTypeDef EraseInitStruct;
  EraseInitStruct.TypeErase = FLASH_TYPEERASE_SECTORS;
  EraseInitStruct.Banks = 1;
  EraseInitStruct.NbSectors = nbsector;
  EraseInitStruct.Sector = get_sector(flash_start_addr);
  EraseInitStruct.VoltageRange = FLASH_VOLTAGE_RANGE_3;
  uint32_t sector_error;
  if (HAL_FLASHEx_Erase(&EraseInitStruct, &sector_error) != HAL_OK)
  {
    Error_Handler();
  }
  HAL_FLASH_Lock();
}

/**
 * The function Flash_Write_Int writes an integer value to a specified address in flash memory.
 *
 * @param address The address parameter is the memory address where the value will be written to. It is
 * of type uint32_t, which means it is an unsigned 32-bit integer. This allows for a larger range of
 * memory addresses to be used.
 * @param value The value parameter is the integer value that you want to write to the specified
 * address in flash memory.
 */
void flash_write_int(uint32_t address, int value)
{
  HAL_FLASH_Unlock();
  HAL_FLASH_Program(FLASH_TYPEPROGRAM_HALFWORD, address, value);
  HAL_FLASH_Lock();
}

/**
 * The function Flash_Write_Float writes a float value to a specified address in flash memory.
 *
 * @param address The address parameter is the memory address where the float value will be written to
 * in the flash memory.
 * @param f The parameter "f" is a floating-point number that you want to write to the flash memory.
 */
void flash_write_float(uint32_t address, float f)
{
  HAL_FLASH_Unlock();
  uint8_t data[4];
  *(float *) data = f;
  HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD, address, *(uint32_t *) data);
  HAL_FLASH_Lock();
}

/**
 * The function Flash_Write_Array writes an array of bytes to a specified address in flash memory.
 *
 * @param address The starting address in flash memory where the array will be written.
 * @param arr The parameter "arr" is a pointer to an array of uint8_t (unsigned 8-bit integer) values.
 * @param leng The parameter "leng" represents the length of the array that needs to be written to the
 * flash memory.
 */
void flash_write_array(uint32_t address, uint8_t *arr, uint16_t leng)
{
  HAL_FLASH_Unlock();
  for (uint16_t i = 0; i < leng; i++)
  {
    HAL_FLASH_Program(FLASH_TYPEPROGRAM_BYTE, address + i, *(arr + i));
  }
  HAL_FLASH_Lock();
}

/**
 * The function "Flash_Write_Struct" writes a structure of type "wifi_info_t" to a specified address in
 * flash memory.
 *
 * @param address The address parameter is the starting address in the flash memory where the data will
 * be written. It is of type uint32_t, which means it is a 32-bit unsigned integer.
 * @param data The "data" parameter is of type "wifi_info_t", which is a user-defined structure that
 * contains information related to WiFi settings or configurations.
 */
void flash_write_struct(uint32_t address, wifi_info_t data)
{
  flash_write_array(address, (uint8_t *) &data, sizeof(data));
}

/**
 * The function Flash_Read_Int reads a 16-bit integer from a specified memory address.
 *
 * @param address The address parameter is of type uint32_t, which means it is an unsigned 32-bit
 * integer. It represents the memory address from which the function will read an integer value.
 *
 * @return The function `Flash_Read_Int` returns an `int` value.
 */
int flash_read_int(uint32_t address)
{
  return *(__IO uint16_t *) (address);
}

/**
 * The function Flash_Read_Float reads a float value from a specific memory address.
 *
 * @param address The address parameter is the memory address from which the float value will be read.
 *
 * @return a float value.
 */
float flash_read_float(uint32_t address)
{
  uint32_t data = *(__IO uint32_t *) (address);
  return *(float *) (&data);
}

/**
 * The function Flash_Read_Array reads an array of bytes from a specified address in flash memory.
 *
 * @param address The starting address from where the data needs to be read from the flash memory.
 * @param arr A pointer to an array where the read data will be stored.
 * @param leng The parameter "leng" represents the length of the array that needs to be read from the
 * flash memory.
 */
void flash_read_array(uint32_t address, uint8_t *arr, uint16_t leng)
{
  for (uint16_t i = 0; i < leng; i++)
  {
    *arr = *(__IO uint8_t *) (address + i);
    arr++;
  }
}

/**
 * The function Flash_Read_Struct reads data from flash memory into a wifi_info_t structure.
 *
 * @param address The address parameter is the starting address in the flash memory from where the data
 * needs to be read. It is of type uint32_t, which means it is a 32-bit unsigned integer. This
 * parameter specifies the memory location from where the data needs to be read.
 * @param data The `data` parameter is a pointer to a `wifi_info_t` structure.
 */
void flash_read_struct(uint32_t address, wifi_info_t *data)
{
  flash_read_array(address, (uint8_t *) data, sizeof(wifi_info_t));
}
/* End of file -------------------------------------------------------- */