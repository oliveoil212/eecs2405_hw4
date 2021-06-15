import sensor, image, time, pyb,math
uart = pyb.UART(3,9600,timeout_char=1000)
uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
tmp = ""
sensor.reset() # Initialize the camera sensor.
sensor.set_hmirror(True)
sensor.set_vflip(True)
sensor.set_pixformat(sensor.RGB565) # use RGB565.
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.
shoter_than_15 = pyb.Pin("P2", pyb.Pin.IN)

def degrees(radians):
    return (180 * radians) / math.pi

while(True):
    clock.tick()
    img = sensor.snapshot()
    tags = img.find_apriltags()
    for tag in tags:
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        #img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        #print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
        #print("%.2f" %degrees(tag.y_rotation()))
        #print(tag)
        y_deg = degrees(tag.y_rotation())
        if y_deg > 180:
            y_deg = 360 - y_deg
        pixel_len = (tag.w()+tag.h())/2
        K = 47 # the pixel len measured in 10cm
        # print('pixel_len =  ', pixel_len)
        distance = K/pixel_len *10
        print('distance = ', distance)
        if distance < 19:
            uart.write("/stop/run \n".encode())
            if distance > 17:
                uart.write("/goStraight/run 50 \n".encode())
            elif distance < 14:
                uart.write("/goStraight/run -50 \n".encode())

        if distance > 16:
            if tag.cx()>100:
                print('turn right')
                uart.write("/turn/run 50 -0.3 \n".encode())
            elif tag.cx() <80:
                print('turn left')
                uart.write("/turn/run 50 0.3 \n".encode())
            else:
                print('go straight')
                uart.write("/goStraight/run 50 \n".encode())
        elif distance < 13:
                print('go back')
                uart.write("/goStraight/run -50 \n".encode())
        else:
            if tag.cx()>100:
                print('turn right')
                uart.write("/turn/run 50 -0.3 \n".encode())
            elif tag.cx() <80:
                print('turn left')
                uart.write("/turn/run 50 0.3 \n".encode())
    if not tags:
        #print('no tag')
        uart.write("/stop/run \n".encode())
    #print(clock.fps())

