## Part1: Parking
video  
https://drive.google.com/file/d/14pp1YX3AWElVIlzwzxCQ96Rof8b-6BQe/view?usp=sharing

## Part2: Line Following
video:  

<!-- https://drive.google.com/file/d/1ekYAl03dRXHfdpLFrryzlREw1HiEld2K/view?usp=sharing -->

https://drive.google.com/file/d/1748YuJUxP1eM58ZqBq5V8IHajRV3jC3Y/view?usp=sharing

## Part3: Position Calibration via AprilTag
video:  

https://drive.google.com/file/d/16rKwLkldmpa_ZfCpIxCDgz4KQ49biHVz/view?usp=sharing

## How to set up
1. copy main.py to your openmv
2. in part3(park3 has all function in part1 and part2 tho) excute 
 ```bash=
sudo mbed compile --source . --source ~/ee2405/mbed-os-build/ -m B_L4S5I_IOT01A -t GCC_ARM -f 
```
3. sudo python3 car_control.py /dev/ttyUSB0

## how to run


| command | para                      | function  |
| ------- | ------------------------- | --------- |
| 1       | direciton, d1(cm), d2(cm) | Part1     |
| 2       | none                      | Part2     |
| 3       | none                      | Part3     |
| t       | none                      | terminate |

