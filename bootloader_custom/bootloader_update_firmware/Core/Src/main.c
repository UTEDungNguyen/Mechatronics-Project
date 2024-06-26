/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2023 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "bootloader.h"
#include "cbuffer.h"
#include "flash.h"
#include "read_hex_file.h"

#include <command_uart_bootloader.h>
#include <stdint.h>
#include <string.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* The above code is defining several constants for different buffer sizes. These constants are used to
specify the size of different buffers used in a C program. */
#define RXBUF_SIZE 8
#define MAINBUF_SIZE 400
#define HANDLEBUF_SIZE 50
#define READBUF_SIZE 1
#define COMMAND_FRAME_SIZE 17

/* The above code is defining three constants: APP_INDICATED_ADDRESS, APP_CURRENT_ADDRESS, and
APP_UPDATE_ADDRESS. These constants represent memory addresses in a C program. */
#define APP_INDICATED_ADDRESS 0x08008000
#define APP_CURRENT_ADDRESS 0x08020000
#define APP_UPDATE_ADDRESS 0x08040000

/* The above code is defining a constant named "SIZE_OF_APP_UPDATE" with a value of 128 * 1024. */
#define SIZE_OF_APP_UPDATE 128 * 1024

/* The above code is defining a constant named "TIME_TO_JUMP_APP_CURRENT" with a value of 3000. */
#define TIME_TO_JUMP_APP_CURRENT 3000
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart1;
DMA_HandleTypeDef hdma_usart1_rx;
DMA_HandleTypeDef hdma_usart1_tx;

/* USER CODE BEGIN PV */
/* The above code is declaring several arrays of type uint8_t and char. These arrays are used for
storing data in a C program. The purpose and usage of these arrays are not clear from the provided
code snippet. */
uint8_t rxbuf[RXBUF_SIZE];
uint8_t mainbuf[MAINBUF_SIZE];
uint8_t read_buffer[READBUF_SIZE];
uint8_t command_buffer[COMMAND_FRAME_SIZE];
char handle_buffer[HANDLEBUF_SIZE];

/* The above code is declaring two character arrays, `ack` and `nack`, each containing a single
character. The character array `ack` is initialized with the character '0', while the character
array `nack` is initialized with the character '1'. */
char ack[1] = "0";
char nack[1] = "1";

uint16_t oldpos = 0;
uint8_t status_command = 0;
uint8_t status_command_handler = 0;
uint8_t flag_cmd = 0;
uint16_t pos_cmd = 0;
uint8_t read_flash_app_update[128] = { 0 };
uint8_t check_fw_app_current[1] = { 0 };
uint8_t check_fw_app_update[1] = { 0 };
uint32_t count_read_app_update;
uint16_t app_indicate = 0;
uint32_t time_jump_start = 0;
uint8_t time_jump_state = 0;

/* Inintial circular buffer from cbuffer */
cbuffer_t cb;

/* Get value of flag in read_hex_file if file hex is wrote done */
extern uint8_t g_flag_write_hex_done;

/**
 * @brief above type defines an enumeration for different status commands.
 *
 */
typedef enum
{
  WAIT_COMMAND,
  WRITE_HEX_COMMAND
} status_command_t;

/**
 * @brief The above type defines an enumeration for indicating the status of a firmware update.
 *
 */
typedef enum
{
  UPDATE_FIRMWARE,
  CURRENT_FIRMWARE = 0xFF
} app_indicate_status_t;

/**
 * @brief The above type defines an enumeration for the status of time to jump.
 *
 */
typedef enum
{
  OLD_FIRMWARE,
  WAIT_NEW_FIRMWARE
} time_to_jump_status_t;

/* The above code is defining a function pointer structure named "handle". This structure contains
pointers to various functions such as HAL_Delay, HAL_UART_Transmit_DMA, ConvertStringtoHex,
Flash_Erase, Flash_Read_Array, and bootloader_jump_address. These function pointers can be used to
call the respective functions in the code. */
function_pointer_t handle = { .ptr_delay = HAL_Delay,
                              .ptr_hal_uart_transmit = HAL_UART_Transmit_DMA,
                              .ptr_convert_string_to_hex = convert_string_to_hex,
                              .ptr_erase_flash = flash_erase,
                              .ptr_read_array = flash_read_array,
                              .ptr_bootloader_jump_to_address = bootloader_jump_address };
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_USART1_UART_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
/**
 * The function HAL_UARTEx_RxEventCallback is a callback function that is called when a receive event
 * occurs on USART1, and it handles the received data by storing it in a circular buffer and resetting
 * the receive buffer.
 *
 * @param huart A pointer to the UART handle structure. It contains information about the UART
 * peripheral being used, such as the base address of the UART registers and the configuration
 * settings.
 * @param Size The parameter "Size" in the function "HAL_UARTEx_RxEventCallback" represents the number
 * of bytes received by the UART peripheral. It indicates the size of the data buffer that has been
 * filled with received data.
 */
void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *huart, uint16_t Size)
{
  if (huart->Instance == USART1)
  {
    /* start the DMA again */
    /* Write rxbuf to the mainbuf */
    cb_write(&cb, rxbuf, Size);
    /* Clear the rxbuf */
    for (uint8_t i = 0U; i < Size; i++)
    {
      rxbuf[i] = '\0';
    }
    /* Check the status command */
    (status_command == WAIT_COMMAND) ? (flag_cmd = 1) : (flag_cmd = 0);
    HAL_UARTEx_ReceiveToIdle_DMA(&huart1, (uint8_t *) rxbuf, RXBUF_SIZE);
    __HAL_DMA_DISABLE_IT(&hdma_usart1_rx, DMA_IT_HT);
  }
}
/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 * @retval int
 */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
  /* Initial circular buffer */
  cb_init(&cb, mainbuf, MAINBUF_SIZE);
  /* Turn on LED on Board (PA5) */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
  /* Read app indicate from Flash */
  app_indicate = (uint8_t) flash_read_int(APP_INDICATED_ADDRESS);
  /* If App Update have new Firmware, Erase Firmware in App Current */
  if (app_indicate == UPDATE_FIRMWARE)
  {
    flash_erase(APP_CURRENT_ADDRESS, 1);
  }
  HAL_UARTEx_ReceiveToIdle_DMA(&huart1, rxbuf, RXBUF_SIZE);
  __HAL_DMA_DISABLE_IT(&hdma_usart1_rx, DMA_IT_HT);
  /* Get the time start Bootloader FW */
  time_jump_start = HAL_GetTick();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    /* Time from the start of the program */
    if ((HAL_GetTick() - time_jump_start) >= TIME_TO_JUMP_APP_CURRENT)
    {
      if (time_jump_state == OLD_FIRMWARE)
      {
        /* Read value in start address of two app */
        flash_read_array(APP_CURRENT_ADDRESS, check_fw_app_current, 1);
        flash_read_array(APP_UPDATE_ADDRESS, check_fw_app_update, 1);
        (check_fw_app_current[0] != 0xFF) ? bootloader_jump_address(APP_CURRENT_ADDRESS)
                                          : (time_jump_start = HAL_GetTick());
      }
    }
    /* Update New FW get from App Update */
    if (app_indicate == UPDATE_FIRMWARE)
    {
      time_jump_state = WAIT_NEW_FIRMWARE;
      /* Read data from App Update and Write to App Current */
      flash_read_array(APP_UPDATE_ADDRESS + count_read_app_update, read_flash_app_update, 128);
      flash_write_array(APP_CURRENT_ADDRESS + count_read_app_update, read_flash_app_update, 128);
      count_read_app_update += 128;
      /* Clear the buffer read_flash_app_update */
      for (uint8_t i = 0U; i < 128; i++)
      {
        read_flash_app_update[i] = 0xFF;
      }
      /* Write full sector */
      if (count_read_app_update >= SIZE_OF_APP_UPDATE)
      {
        /* Erase App Indicate and App Update */
        flash_erase(APP_INDICATED_ADDRESS, 1);
        flash_erase(APP_UPDATE_ADDRESS, 1);
        /* Jump to App Current */
        bootloader_jump_address(APP_CURRENT_ADDRESS);
      }
    }
    /* No Firmware to Update */
    else if (app_indicate == CURRENT_FIRMWARE)
    {
      /* Check the write pointer and read pointer */
      if (cb_check_read_wrire_ptr(&cb) == 0)
      {
        /* read from mainbuf and assign into read_buffer */
        cb_read(&cb, read_buffer, 1);
        /* Wait Command */
        if (status_command == WAIT_COMMAND)
        {
          if (flag_cmd == 1)
          {
            /* Write read_buffer into command_buffer */
            command_buffer[pos_cmd] = read_buffer[0];
            pos_cmd++;
            /* Frame of Command is 17 */
            if (pos_cmd == COMMAND_FRAME_SIZE)
            {
              pos_cmd = 0;
              /* Handle Command and assign to status_command_handler*/
              status_command_handler = command_handler(&handle, (char *) command_buffer, COMMAND_FRAME_SIZE);
              /* Write command */
              if (status_command_handler == WRITE_COMMAND)
              {
                status_command = WRITE_HEX_COMMAND;
                time_jump_state = WAIT_NEW_FIRMWARE;
              }
              /* Command fail */
              else if (status_command_handler == COMMAND_FAIL)
              {
                HAL_UART_Transmit_DMA(&huart1, (uint8_t *) "Run command fail", 16);
              }
              /* Other Command like: Read, Erase, Jump */
              else
              {
                time_jump_start = HAL_GetTick();
                time_jump_state = OLD_FIRMWARE;
              }
            }
          }
        }
        /* Write command */
        else
        {
          /* Check the last one line of hex file */
          if (read_buffer[0] != '\n' && read_buffer[0] != '\r')
          {
            /* assign read_buffer to handle_buffer */
            handle_buffer[oldpos] = read_buffer[0];
            oldpos++;
          }
          /* Check the last one line of hex file */
          if (read_buffer[0] == '\n')
          {
            /* Hanlde Hex File and return ack */
            if (read_all_line(handle_buffer, oldpos) == READ_SUCCESSFULLY)
            {
              HAL_UART_Transmit_DMA(&huart1, (uint8_t *) ack, 1);
              /* Get g_flag_write_hex_done from read_hex_file to get event write flag to App Indicate */
              if (g_flag_write_hex_done == 1)
              {
                /* Write flag to App Indicate */
                flash_write_int(APP_INDICATED_ADDRESS, UPDATE_FIRMWARE);
                status_command = WAIT_COMMAND;
                g_flag_write_hex_done = 0;
                time_jump_state = OLD_FIRMWARE;
                time_jump_start = HAL_GetTick();
              }
            }
            /* If Read Fail return nack */
            else
            {
              HAL_UART_Transmit_DMA(&huart1, (uint8_t *) nack, 1);
            }
            /* Clear the handle buffer */
            for (uint8_t i = 0U; i < HANDLEBUF_SIZE; i++)
            {
              handle_buffer[i] = '\0';
            }
            /* Reset index to 0 */
            oldpos = 0;
          }
        }
      }
    }
  }
  /* USER CODE END 3 */
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = { 0 };
  RCC_ClkInitTypeDef RCC_ClkInitStruct = { 0 };

  /** Configure the main internal regulator output voltage
   */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the RCC Oscillators according to the specified parameters
   * in the RCC_OscInitTypeDef structure.
   */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
   */
  RCC_ClkInitStruct.ClockType =
    RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
 * @brief USART1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_USART1_UART_Init(void)
{
  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 57600;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */
}

/**
 * Enable DMA controller clock
 */
static void MX_DMA_Init(void)
{
  /* DMA controller clock enable */
  __HAL_RCC_DMA2_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA2_Stream2_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream2_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream2_IRQn);
  /* DMA2_Stream7_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream7_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream7_IRQn);
}

/**
 * @brief GPIO Initialization Function
 * @param None
 * @retval None
 */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = { 0 };

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);

  /*Configure GPIO pin : PA5 */
  GPIO_InitStruct.Pin = GPIO_PIN_5;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef USE_FULL_ASSERT
/**
 * @brief  Reports the name of the source file and the source line number
 *         where the assert_param error has occurred.
 * @param  file: pointer to the source file name
 * @param  line: assert_param error line source number
 * @retval None
 */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line
     number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
