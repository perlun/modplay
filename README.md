## modplay

Simple tool for playing `.mod` files (and some other formats) with GPIO-based
visualization for Raspberry Pi.

Does not work on platforms where `RPi.GPIO` is not supported

### What it looks like in action

(YouTube link. Module played is [`axelf_8.mod`](https://modarchive.org/index.php?request=view_by_moduleid&query=34469) by Scott Wilkins. Thank you!)

[![Modplayer with 8-channel Raspberry Pi LED visualization](https://img.youtube.com/vi/3TEI_KRq3IY/maxresdefault.jpg)](https://www.youtube.com/watch?v=3TEI_KRq3IY)

### Requirements

(Tested on Debian bookworm, i.e. not Raspbian, but should be fine there as
well.)

```bash
$ apt-get install python3-pip
$ pip install miniaudio libxmplite
```

### Use

`sudo` is unfortunately required for `/dev/kmem` access, needed by `RPi.GPIO`.

```bash
$ sudo ./modplay <file>
```

### GPIO wireout

Only 8 channels are currently supported; it feels a bit exaggerated to connect
more GPIO pins than that to your breadboard. :) Theoretically, it should be
possible to extend this to a theoretical maximum of 28 channels, if I count the
number of GPIO pins correctly on https://pinout.xyz/

Remember to connect a suitable ground pin, e.g. GPIO pin 6, to the other
(positive) side of the breadboard, and **remember to use resistors**. You may
otherwise break both your LEDs and the components in your RPi.

- Channel 0: GPIO 18 (pin 12)
- Channel 1: GPIO 23 (pin 16)
- Channel 2: GPIO 24 (pin 18)
- Channel 3: GPIO 25 (pin 22)
- Channel 4: GPIO 8 (pin 24)
- Channel 5: GPIO 7 (pin 26)
- Channel 6: GPIO 1 (pin 28)
- Channel 7: GPIO 12 (pin 32)

### License (zlib license)

Copyright (c) 2023 Per Lundberg

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.
