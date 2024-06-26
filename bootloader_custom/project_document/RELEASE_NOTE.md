# RELEASE NOTE: STEP COUNTING DEVICE USER GUIDE

## Components:

**1. STM32F411RE - Nucleo Board:** The central processing unit and control hub of the wearable device.
**2. MPU6050 3-axis Gyro Sensor:** For precise motion detection, enabling accurate step counting.
**3. Module MFRC522:** Identify user ID
**4. OLED Screen:** Displays real-time clock information such as step count and user recognition status.
**5. DS1307:** Provide real-time clock information

##New Features - Key Highlights:

**1. Adding New IDs for Counting:**

- You can now add a new device for step counting by providing a unique ID for that device.
- The system will start counting steps for the new device and record the corresponding step count for that ID.

**2. Firmware Update via Bootloader user UART:**

- You can easily update the device's firmware by connecting it to a computer and using the integrated bootloader.
- The bootloader allows you to safely and easily load a new firmware version onto the device.
 
**3. Data Backup During Power Loss:**

- The SmartStep Tracker features data backup functionality, ensuring that step count data is not lost during power outages.
- Once power is restored, the device will restore the backed-up data and continue step counting as usual.

**4. Using the RTC (Real-Time Clock):**

- The integrated RTC helps you track the real-time when events like step counting occurred.
- This enables data synchronization with real-time, allowing for accurate activity monitoring.

## STEP COUNTING DEVICE USER GUIDE:

***Step 1: Activate the Device:***

- Load the program into the MCU
- The OLED screen will display status information and readiness for operation.

***Step 2: Set ID_Card:***

- Each user will be assigned a unique ID_Card with a distinct ID number.
- Place your ID_Card near the device to initiate step counting.

***Step 3: Use Step Counting Device:**

- Now, you can start moving or exercising.
- The device will utilize a 3-axis accelerometer to track motion and count the number of steps you take.

***Step 4: Monitor Step Count:***

- During use, the OLED screen will display your step count along with real-time activity information.

***Step 5: Stop Step Counting:***

- To stop step counting, place your ID_Card near the device once again.
 
## Important Notes:
- Always carry your ID_Card to use the device.
- When changing users or starting a new step count session, reset your ID_Card.
- The program has set the default time for RTC.