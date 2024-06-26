/**
 * @file        bootloader.c
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Includes ----------------------------------------------------------- */
#include "bootloader.h"

/**
 * The function `bootloader_jump_address()` sets up the necessary configurations and jumps to a
 * specified address to start executing code.
 */
void bootloader_jump_address(uint32_t jump_to_address)
{
  /* Turn off Peripheral, Clear Interrupt Flag*/
  HAL_RCC_DeInit();

  /* Clear Pending Interrupt Request, turn  off System Tick*/
  HAL_DeInit();

  /* Turn off fault harder*/
  SCB->SHCSR &= ~(SCB_SHCSR_USGFAULTENA_Msk | SCB_SHCSR_BUSFAULTENA_Msk | SCB_SHCSR_MEMFAULTENA_Msk);

  /* Set Main Stack Pointer*/
  __set_MSP(*((volatile uint32_t *) jump_to_address));

  uint32_t bootloader_jump = *((volatile uint32_t *) (jump_to_address + 4));

  /* Set Program Counter to Blink LED Apptication Address*/
  void (*reset_handler)(void) = (void *) bootloader_jump;
  reset_handler();
}
