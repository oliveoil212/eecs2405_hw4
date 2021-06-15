#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"
BufferedSerial pc(USBTX, USBRX);
BufferedSerial xbee(D1, D0);
BufferedSerial openmv(A1, A0);
Ticker servo_ticker;
Ticker encoder_ticker;
PwmOut pin5(D11), pin6(D13);
DigitalIn encoder(D12);
volatile int steps;
volatile int last;
BBCar car(pin5, pin6, servo_ticker);
void encoder_control() {
   int value = encoder;
   if (!last && value) steps++;
   last = value;
}
// void BBCar::goStraight_cm( double speed, double len ){
//     servo0.set_factor(1);
//     servo1.set_factor(1);
//     servo0.set_speed(100);
//     servo1.set_speed(-100);
//     if(len > 19) {
//         // car.goStraight(100); /// 100 1 19.5 100 0.5 7.5cm 100 0.25 3c,
//         ThisThread::sleep_for((1000 * len /19.5)ms);
//     } else if (len > 7) {
//         // car.goStraight(100); /// 100 1 19.5 100 0.5 7.5cm 100 0.25 3c,
//         ThisThread::sleep_for((500 * len /7.5)ms);
//     }else {
//         // car.goStraight(100); /// 100 1 19.5 100 0.5 7.5cm 100 0.25 3c,
//         ThisThread::sleep_for((250 * len /3)ms);
//     }
// }
void openmvserial(){
   char buf[256], outbuf[256];
   FILE *devin = fdopen(&openmv, "r");
   FILE *devout = fdopen(&openmv, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}
int main() {
   encoder_ticker.attach(&encoder_control, 10ms);
   Thread t;
   t.start(&openmvserial);
   char buf[256], outbuf[256];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while (1) {
      memset(buf, 0, 256);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         buf[i] = fputc(recv, devout);
      }
   RPC::call(buf, outbuf);
   }
}



// int  main() {
//    // pc.set_baud(9600);
//    encoder_ticker.attach(&encoder_control, 10ms);
//    steps = 0;
//    last = 0;
//    car.goStraight(200);
//    while(steps*6.5*3.14/32 < 15) {
//       printf("encoder = %d\r\n", steps);
//       ThisThread::sleep_for(100ms);
//    }
//    car.stop();

//    car.spin(200);
//    ThisThread::sleep_for(700ms);
//    car.stop();

//    steps = 0;
//    last = 0;
//    car.goStraight(200);
//    while(steps*6.5*3.14/32 < 20) {
//       printf("encoder = %d\r\n", steps);
//       ThisThread::sleep_for(100ms);
//    }
//    car.stop();
// }
