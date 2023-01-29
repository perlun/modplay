#!/usr/bin/python3

#
# Based on https://github.com/irmen/pylibxmplite/blob/8c79b939c9e9ad7a07fe9cb64e68158b32908974/examples/modplay.py (MIT licensed)
#

import sys
import miniaudio
import libxmplite
import RPi.GPIO as GPIO
import atexit

# Note: this means we only support modules with up to 8 channels. Right now, the
# player will probably naively crash if you try to use it with a module with
# more channels than that.
GPIO_PIN_BY_CHANNEL = [
    18,
    23,
    24,
    25,

    8,
    7,
    1,
    12
]

class Display:
    def __init__(self, mod_info: libxmplite.ModuleInfo) -> None:
        self.mod_info = mod_info

    def update(self, info: libxmplite.FrameInfo) -> None:
        self.cls()
        print("PLAYING MODULE: ", self.mod_info.name)
        print("  (", self.mod_info.type, " ", self.mod_info.chn, "channels ", self.mod_info.bpm, "bpm )")
        print("\n#", info.time, "/", info.total_time, "  pos", info.pos, " pat", info.pattern, " row", info.row, "\n")

        i = 0
        for ch in info.channel_info[:mod_info.chn]:
            if ch.event:
                gpio_enable(i)
            else:
                gpio_disable(i)

            print("*" if ch.event else " ", "I{:03d} #{:03d}".format(ch.instrument, ch.note), end="")
            volume = "#" * int((ch.volume / mod_info.gvl) * mod_info.vol_base / 2)
            print(" |", volume.ljust(mod_info.vol_base // 2, " "), "|")

            i += 1

        print("\nPress Enter to quit.", flush=True)

    def cls(self) -> None:
        print("\033[2J\033[H", end="")


def stream_module(xmp: libxmplite.Xmp, display: Display):
    required_frames = yield b""  # generator initialization
    try:
        while True:
            buffer = xmp.play_buffer(required_frames * 2 * 2)
            display.update(xmp.frame_info())
            required_frames = yield buffer
    except libxmplite.XmpError as x:
        print("XMP Playback error!!", x)


def gpio_init():
    # Enable output mode for our desired GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)

    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(1, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)


def enable_led(num):
    GPIO.output(num, GPIO.HIGH)


def disable_led(num):
    GPIO.output(num, GPIO.LOW)


def gpio_enable(i):
    enable_led(GPIO_PIN_BY_CHANNEL[i])


def gpio_disable(i):
    disable_led(GPIO_PIN_BY_CHANNEL[i])


def disable_leds():
    for i in GPIO_PIN_BY_CHANNEL:
        disable_led(i)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("must give mod filename to play as argument")

    gpio_init()
    atexit.register(disable_leds)

    device = miniaudio.PlaybackDevice(output_format=miniaudio.SampleFormat.SIGNED16, nchannels=2, sample_rate=44100)

    xmp = libxmplite.Xmp()
    xmp.load(sys.argv[1])
    xmp.start(device.sample_rate)

    mod_info = xmp.module_info()
    display = Display(mod_info)
    stream = stream_module(xmp, display)
    next(stream)  # start the generator
    device.start(stream)

    print("\nFile playing in the background. Press Enter to stop playback!\n")

    try:
        input()
    except KeyboardInterrupt:
        # No need to do anything here since the lines below will quit the playback
        pass

    xmp.stop()
    xmp.release()
    device.close()
