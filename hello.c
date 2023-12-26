#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>
int main (void)
{
    int fd ;
    fd = serialOpen ("/dev/ttyAMA0", 9600);
    wiringPiSetup ();
    printf("serial test begin... \n");
    serialPrintf(fd, "Hello guys \n");
    serialPrintf(fd, "Dungdeptrai \n");
    while (1){
        while (serialDataAvail (fd)){
            serialPutchar(fd, serialGetchar(fd)) ;
        }
    }
    serialClose(fd) ;
    return 0 ;
}