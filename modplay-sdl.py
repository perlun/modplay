#!/usr/bin/python3

# Based on an example from a forum (URL forgotten)

# `apt-get install python3-pygame` to be able to run this on Debian GNU/Linux.

from time import sleep
from pygame import mixer
import sys

mixer.init()
music = mixer.music
music.load(sys.argv[1])
music.play(loops=-1)

while True:
    print(music.get_busy())

    # TODO: Would like to get the status of the channels here, but the problem
    # TODO: is that PyGame doesn't expose any such thing to us. All the calls
    # TODO: below return False perpetually.

    # print(mixer.Channel(0).get_busy())
    # print(mixer.Channel(1).get_busy())
    # print(mixer.Channel(2).get_busy())
    # print(mixer.Channel(3).get_busy())
    # print(mixer.Channel(4).get_busy())
    # print(mixer.Channel(5).get_busy())
    # print(mixer.Channel(6).get_busy())
    # print(mixer.Channel(7).get_busy())
    sleep(1)
