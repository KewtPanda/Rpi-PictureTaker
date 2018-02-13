#!/usr/bin/python3

from picamera import PiCamera
from time import sleep
from sys import argv
import numpy as np
import io
import cv2



class Camera:
    # Camera constructor setting base values to the camera
    def __init__(self):
        self.camera = PiCamera()
        # default camera settings
        self.resolution            = [2592, 1944] # max resolution: (2592, 1944) for 1.13 and () for 2.1
        self.framerate             = 15           # default --
        self.brightness            = 50           # default 50
        self.contrast              =  0           # default 0
        self.sharpness             =  0           # default 0
        self.saturation            =  0           # default 0
        self.iso                   =  0           # default 0
        self.shutter_speed         =  0           # default 0
        self.exposure_speed        =  0           # default 0
        self.exposure_compensation =  0           # default 0
        self.exposure_mode         = 'auto'       # default 'auto'
        self.awb_mode              = 'auto'       # default 'auto'
        self.awb_gains             = 0            # default disabled when awb_mode is auto
        self.video_stabilization   = False        # default False
        self.meter_mode            = 'average'    # default 'average'
        self.image_effect          = 'none'       # default 'none'
        self.color_effects         = None         # default None
        self.rotation              = 0            # default 0
        self.hflip                 = False        # default False
        self.vflip                 = False        # default False
        self.zoom                  = [0.0, 0.0, 1.0, 1.0]

    # check command-line arguments
    def parameters(self):    
        for i in range(1, len(argv)):
            if argv[i] == '-help':
                self.help_msg()
                self.camera.close()
                raise SystemExit('Start program with new values')
            elif argv[i] == '-resolution':
                self.resolution = [int(argv[i+1]), int(argv[i+2])]
            elif argv[i] == '-framerate':
                self.framerate = int(argv[i+1])
            elif argv[i] == '-brightness':
                self.brightness = int(argv[i+1])
            elif argv[i] == '-contrast':
                self.contrast = int(argv[i+1])
            elif argv[i] == '-sharpness':
                self.sharpness = int(argv[i+1])
            elif argv[i] == '-saturation':
                self.saturation = int(argv[i+1])
            elif argv[i] == '-iso':
                self.iso = int(argv[i+1])
            elif argv[i] == '-shutter_speed':
                self.shutter_speed = float(argv[i+1])
            elif argv[i] == '-exposure_speed':
                self.exposure_speed = float(argv[i+1])
            elif argv[i] == '-exposure_compensation':
                self.exposure_compensation = int(argv[i+1])
            elif argv[i] == '-exposure_mode':
                self.exposure_mode = argv[i+1]
            elif argv[i] == '-awb_mode':
                self.awb_mode = argv[i+1]
            elif argv[i] == '-awb_gains':
                self.awb_gains = float(argv[i+1])
            elif argv[i] == '-video_stabilization':
                self.video_stabilization = True
            elif argv[i] == '-meter_mode':
                self.meter_mode = argv[i+1]
            elif argv[i] == '-image_effect':
                self.image_effect = argv[i+1]
            elif argv[i] == '-color_effects':
                self.color_effects = argv[i+1]
            elif argv[i] == '-rotation':
                self.rotation = int(argv[i+1])
            elif argv[i] == '-hflip':
                self.hflip = True
            elif argv[i] == '-vflip':
                self.vflip = True
            elif argv[i] == '-zoom':
                self.zoom = [float(argv[i+1]), float(argv[i+2]), float(argv[i+3]), float(argv[i+4])]
    
    # help function that writes all the options available
    def help_msg():
        print('')
        print('-resolution 2592 1944      #default 2592 1944')
        print('-framerate 15              #default 15')
        print('-brightness 50             #default 50      -->    0 - 100')
        print('-contrast 0                #default  0      --> -100 - 100')
        print('-sharpness 0               #default  0      --> -100 - 100')
        print('-saturation 0              #default  0      --> -100 - 100')
        print('-iso 0                     #default  0      -->    0 - 1600. 0 is auto. (Disabled when exposure_mode is off)')
        print('-shutter_speed 0           #default  0      --> 0 is auto. If framerate is 30, shutter_speed cannot be slower than 33,333us (1/framerate)')
        print('-exposure_speed 0          #default  0      --> ')
        print('-exposure_compensation 0   #default  0      -->  -25 - 25. 6 increase exposure by 1 stop')
        print('-exposure_mode auto        #default auto    -->  auto, off, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks')
        print('-awb_mode auto             #default auto    -->  auto, off, sunlight, cloudy, shade, tungsten, fluorescent, incandescent, flash, horizon')
        print('-awb_gains 1.4             #default --      -->  0.0 - 8.0, mostly 0.9 - 1.9. (awb_mode must be off)')
        print('-video_stabilization       #default False')
        print('-meter_mode average        #default average --> average, spot, backlit, matrix. ')
        print('-image_effect none         #default none    --> none, negative, solarize, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur, saturation, colorswap, washedout, posterise, colorpoint, colorbalance, cartoon, deinterlace1, deinterlace2')
        #print('-color_effects None        #default None    --> 128 128 makes iamge black and white. 0 - 255')
        print('-rotation 0                #default  0      --> 0, 90, 180, 270')
        print('-hflip                     #default False')
        print('-vflip                     #default False')
        print('-zoom 0.0 0.0 1.0 1.0      #default 0.0 0.0 1.0 1.0. (x, y, w, h) from 0.0 - 1.0')
        print('')

    # set camera values
    def update(self):
        try:
            self.camera.resolution = self.resolution
            self.camera.framerate = self.framerate
            self.camera.brightness = self.brightness
            self.camera.contrast = self.contrast
            self.camera.sharpness = self.sharpness
            self.camera.saturation = self.saturation
            self.camera.iso = self.iso
            #camera.shutter_speed = camera.exposure_speed
            self.camera.exposure_compensation = self.exposure_compensation
            self.camera.exposure_mode = self.exposure_mode
            self.camera.awb_mode = self.awb_mode
            self.camera.awb_gains = self.awb_gains
            self.camera.video_stabilization = self.video_stabilization
            self.camera.meter_mode = self.meter_mode
            self.camera.image_effect = self.image_effect
            self.camera.color_effects = self.color_effects
            self.camera.rotation = self.rotation
            self.camera.hflip = self.hflip
            self.camera.vflip = self.vflip
            self.camera.zoom = self.zoom
        except:
            print('Failed to set camera values!')
            self.camera.close()



# main function
def main():
    camera = Camera() # Create a new camera object
    camera.parameters() # Check for camera parameters from command line
    camera.update() # Update camera parameters)
    #camera.EXPOSURE_MODES # used to loop over available exposure modes
    #camera.AWB_MODES # used to loop over available awb modes
    
    stream = io.BytesIO()

    camera.camera.start_preview() # use (alpha=200) to get transparent preview

    try:
        sleep(2)
        camera.capture(stream, format='jpeg')
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
        image = image[:, :, ::-1]

            
                


        # close camera to free resources
        pass
    finally:
        camera.camera.stop_preview()
        camera.camera.close()


# call the main function when the program start
if __name__ == '__main__':
    main()
