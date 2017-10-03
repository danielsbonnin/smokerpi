 /***/
/** kType.c: Read k-type thermocouple on raspberry pi using max6675 chip
 * (must be compiled with -lwiringpi flag)
 * */
#define CLK 5
#define DBIT 6 // so
#define CS 7

#include <wiringPi.h>
#include <stdlib.h>
#include <stdio.h>

// declare function
int Thermal_Couple_Read(void);

int SENSOR_VALUE = 0;
float Ctemp, Ftemp;
int type = 0;
int main(int argc, char* argv[])   {
  if (wiringPiSetup () == -1)
    exit (1) ;

  pinMode(CLK, OUTPUT);
  pinMode(DBIT, INPUT);
  pinMode(CS, OUTPUT);

  digitalWrite(CS, HIGH);
  digitalWrite(CLK, LOW);

  SENSOR_VALUE = Thermal_Couple_Read();
  if (SENSOR_VALUE == -1)   {
    printf ("-666");
  }
  else  {
    Ctemp = SENSOR_VALUE * 0.25;
    if (argc > 1) {
      if (strcmp(argv[1], "F") == 0) {
        Ftemp = (Ctemp * 9 / 5) + 32;
        printf ("%4.2f", Ftemp);
      }
      else if (strcmp(argv[1], "C") == 0) {
        printf("%4.2f", Ctemp);
      }
    }
    else {
      Ftemp = (Ctemp * 9 / 5) + 32;
      printf ("%4.2f", Ftemp);
    }
  }
  return 0;
}

int Thermal_Couple_Read()   {

  int value = 0;
  // init sensor
  digitalWrite(CS, LOW);
  delay(2);
  digitalWrite(CS, HIGH);
  delay(200);

  /* Read the chip and return the raw temperature value
  Bring CS pin low to allow us to read the data from
  the conversion process */

  digitalWrite(CS, LOW);
  /* Cycle the clock for dummy bit 15 */
  digitalWrite(CLK, HIGH);
  // delay(1);
  digitalWrite(CLK, LOW);

  /*
  Read bits 14-3 from MAX6675 for the Temp.
  Loop for each bit reading
  the value and storing the final value in 'temp' */

  int i;
  for (i = 14; i >= 0; i--) {
    digitalWrite(CLK, HIGH);
    // delay(1);
    value += digitalRead(DBIT) << i;
    digitalWrite(CLK, LOW);
  }

  // check bit D2 if HIGH no sensor
  if ((value & 0x04) == 0x04) return -1;
  // shift right three places
  return value >> 3;

}
