/**
 * @file        cbuffer.c
 * @author      Dung Nguyen
 * @brief
 * @version     1.0.0
 * @date        2023-08-09
 *
 */

/* Includes ----------------------------------------------------------- */
#include "cbuffer.h"

/* Private defines ---------------------------------------------------- */
/* Private enumerate/structure ---------------------------------------- */
/* Private macros ----------------------------------------------------- */
/* Public variables --------------------------------------------------- */
/* Private variables -------------------------------------------------- */
/* Private function prototypes ---------------------------------------- */
/* Function definitions ----------------------------------------------- */
// Initialize the Circular buffer with a size of ... bytes
void cb_init(cbuffer_t *cb, void *buf, uint32_t size)
{
  cb->data = (uint8_t *) buf;
  cb->size = size;
  cb->writer = 0;
  cb->reader = 0;
  cb->overflow = 0;
  cb->active = true;
}

// Clear and set pointer to the original position
void cb_clear(cbuffer_t *cb)
{
  cb->writer = 0;
  cb->reader = 0;
  cb->overflow = 0;
}

// Count the number of elements
uint32_t cb_data_count(cbuffer_t *cb)
{
  if (cb->writer >= cb->reader)
  {
    return cb->writer - cb->reader;
  }

  else
  {
    return cb->size + cb->writer - cb->reader;
  }
}

// Count the number of empty elements
uint32_t cb_space_count(cbuffer_t *cb)
{
  return cb->size - cb_data_count(cb);
}

// Check buffer is full or not in case write buffer
static bool cb_is_full(cbuffer_t *cb, uint32_t nbytes)
{
  return cb_space_count(cb) < nbytes;
}

// Check buffer is empty or not in case read buffer
static bool cb_is_empty(cbuffer_t *cb)
{
  return cb_data_count(cb) == 0;
}

// Check buffer is empty or not in case read buffer
bool cb_check_read_wrire_ptr(cbuffer_t *cb)
{
  return (cb->writer == cb->reader) ? 1 : 0;
}

// Function to read a buffer
uint32_t cb_read(cbuffer_t *cb, void *buf, uint32_t nbytes)
{
  // In case read buffer, reader pointer is allowed to touch writer pointer
  // If writer pointer = reader pointer or circular buffer is empty ==> read 0 byte
  if (cb_is_empty(cb))
  {
    return 0;
  }

  uint32_t bytes_to_read = (nbytes > cb_data_count(cb)) ? cb_data_count(cb) : nbytes;

  if (cb->reader + bytes_to_read < cb->size)
  {
    memcpy(buf, &cb->data[cb->reader], bytes_to_read);
    cb->reader += bytes_to_read;
  }

  else
  {
    uint32_t bytes_until_end = cb->size - cb->reader;
    memcpy(buf, &cb->data[cb->reader], bytes_until_end);
    uint32_t remaining_bytes = bytes_to_read - bytes_until_end;
    memcpy(&((uint8_t *) buf)[bytes_until_end], &cb->data[0], remaining_bytes);
    cb->reader = remaining_bytes;
  }

  return bytes_to_read;
}

// Function to write a buffer
uint32_t cb_write(cbuffer_t *cb, void *buf, uint32_t nbytes)
{
  // If circular buffer is full ==> write 0 byte
  // Writer pointer is not touch reader pointer (limit writer pointer+1 = cb->size)
  // If Writer pointer after write and touch reader pointer ==> write 0 byte
  if (cb_is_full(cb, nbytes))
  {
    cb->overflow++;
    return 0;
  }

  uint32_t bytes_to_write = (nbytes > cb_space_count(cb)) ? cb_space_count(cb) : nbytes;

  if (cb->writer + bytes_to_write < cb->size)
  {
    memcpy(&cb->data[cb->writer], buf, bytes_to_write);
    cb->writer += bytes_to_write;
  }

  else
  {
    uint32_t bytes_until_end = cb->size - cb->writer;
    memcpy(&cb->data[cb->writer], buf, bytes_until_end);
    uint32_t remaining_bytes = bytes_to_write - bytes_until_end;
    memcpy(&cb->data[0], &((uint8_t *) buf)[bytes_until_end], remaining_bytes);
    cb->writer = remaining_bytes;
  }

  return bytes_to_write;
}
/* End of file -------------------------------------------------------- */