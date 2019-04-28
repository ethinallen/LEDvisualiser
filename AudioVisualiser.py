import time, pyaudio, wave, sys, serial
import numpy as np
from base64 import b16encode
from pyfirmata import Arduino, util

arduino = serial.Serial('/dev/cu.usbmodem1411', 9600)

# import portaudio
CHUNK = 2**12 ## used to be 11 before I changed it; if it fucks up it is most definitely because i change the chunk size
FORMAT = pyaudio.paInt16
# the format of the audio (pyaudio reference)
CHANNELS = 2
# Number of channels
RATE = 44100
# scan rate
isRunning = True
isPlaying = True
# turtle.colormode(255)
# sets turtle color to rgb 255 values
BLACK = (0,0,0)
p = pyaudio.PyAudio()
colorMult = 0

# starts pyaudio

stream = p.open(format = pyaudio.paInt16, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
# starts stream

def color(angle):
    red = np.sin(angle)
    green = np.sin(angle + 60)
    blue = np.sin(angle + 120)
    return (red, green, blue)

while isRunning:
    data = np.fromstring(stream.read(CHUNK, exception_on_overflow = False), dtype=np.int16)
    peak = np.average(np.abs(data))*2
    bars = '#'*int(250*peak/2**16)
    print('%05d %s'%(peak,bars))
    brightness = int(250*peak/2**16)
    print(brightness)
    brightnessMult = brightness*255/200
    # use this to get the intensity ---> brightness of node
    if brightnessMult > 255:
        brightnessMult = 255
    if brightnessMult < 15:
        brigtnessMult = 0

    data = np.fromstring(stream.read(CHUNK), dtype = np.int16)
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)]
    freq = np.fft.fftfreq(CHUNK, 1.0/44100)
    freqPeak = freq[np.where(fft==np.max(fft))[0][0]] + 1
    angle = 360*freqPeak/150000

    # colorMult = brightness/
    red = 100 * np.sin(angle)
    green = 100 * np.sin(angle + 60)
    blue = 100 * np.sin(angle + 120)

    if red < 0:
        red = 0
    if green < 0:
        green = 0
    if blue < 0:
        blue = 0
# turns off the pixel if it's not in range, reflective of nature of np.sin function

    if isPlaying:
        # print(brightness)
        if freqPeak <= 5:
            color = (0,0,0)
        else:
            color = (int(red), int(green), int(blue))
        print (color)
        arduino.write(color)
        #time.sleep(1/360)
    # else:
    #     color = (BLACK)
stream.stopstream()
stream.close()
p.terminate()
