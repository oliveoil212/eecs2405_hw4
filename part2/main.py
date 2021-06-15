import sensor, image, time, pyb
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

# For color tracking to work really well you should ideally be in a very, very,
# very, controlled enviroment where the lighting is constant...
green_threshold   = (6,46,-10,9,-27,-6)
size_threshold = 2000


def find_max(blobs):
    max_size=0
    max_blob = blobs[0]
    for blob in blobs:
        y_bot = blob.y() + blob.h()
        if blob[2]*blob[3] > max_size :
            if y_bot > 50:
                max_blob=blob
                max_size = blob[2]*blob[3]
    return max_blob

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    blobs = img.find_blobs([green_threshold])
    if blobs:
        max_blob = find_max(blobs)
        img.draw_rectangle(max_blob[0:4]) # rect
        img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
        #print(max_blob)
        mean_x = max_blob.x() + max_blob.w()/2
        diff = mean_x - 80
        turn_thershold = 40
        if abs(diff) >turn_thershold:
            if diff < 0:
                uart.write("/turn/run 50 0.3 \n".encode())
                print('turn left')
            else:
                uart.write("/turn/run 50 -0.3 \n".encode())
                print('turn right')
        else:
            uart.write("/goStraight/run 100 \n".encode())
            print('go straight')
        #time.sleep(0.3)
        #print(mean_x)
        #uart.write(("%.2f \r\n" %mean_x).encode())
    else:
        uart.write("/stop/run \n".encode())
