import time
import serial
import sys,tty,termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
    if k=='\x1b':
        k2 = inkey()
        k3 = inkey()
        if k3=='A':
            print ("up")
            s.write("/goStraight/run 100 \n".encode())
        if k3=='B':
            print ("down")
            s.write("/goStraight/run -100 \n".encode())
        if k3=='C':
            print ("right")
            s.write("/turn/run 100 -0.3 \n".encode())
        if k3=='D':
            print ("left")
            s.write("/turn/run 100 0.3 \n".encode())
        time.sleep(1)
        s.write("/stop/run \n".encode())
    elif k=='q':
        print ("quit")
        return 0
    elif k=='s' :
        print ("spin")
        s.write("/spin/run 100 \n".encode())
        time.sleep(0.5)
        s.write("/stop/run \n".encode())
    elif k=='p' :
        print ("park")
        para = input()
        command = '/goParking/run ' + para + ' \n'
        print(command)
        s.write(command.encode())
        time.sleep(1.5)
        # s.write("/stop/run \n".encode())
    elif k=='o':
        s.write('/goParking/run 15 15 0 \n'.encode())
    elif k=='m':
        mode = input('0 for line  1 for apriltag\n')
        command = '/mode_pin/write ' + mode + ' \n'
        s.write(command.encode())
        time.sleep(0.5)
        command = '/enable_pin/write 1 \n'
        s.write(command.encode())
    elif k == 't':
        command = '/enable_pin/write 0 \n'
        s.write(command.encode())
        time.sleep(1)
        command = '/mode_pin/write 0 \n'
        s.write(command.encode())
        time.sleep(1)
        s.write("/stop/run \n".encode())
        print('terminate')
    elif k == 'g':
        # mode = 1
        command = '/mode_pin/write 1' + ' \n'
        s.write(command.encode())
        time.sleep(0.5)
        command = '/enable_pin/write 1 \n'
        s.write(command.encode())
    else:
        print ("not an arrow key!")
    return 1

if len(sys.argv) < 1:
    print ("No port input")
s = serial.Serial(sys.argv[1])
while get():
    i = 0
