#!/usr/bin/python3

#
# Based on https://github.com/irmen/pylibxmplite/blob/8c79b939c9e9ad7a07fe9cb64e68158b32908974/examples/modplay.py (MIT licensed)
#

import sys
import miniaudio
import libxmplite


class Display:
    def __init__(self, mod_info: libxmplite.ModuleInfo) -> None:
        self.mod_info = mod_info

    def update(self, info: libxmplite.FrameInfo) -> None:
        self.cls()
        print("PLAYING MODULE: ", self.mod_info.name)
        print("  (", self.mod_info.type, " ", self.mod_info.chn, "channels ", self.mod_info.bpm, "bpm )")
        print("\n#", info.time, "/", info.total_time, "  pos", info.pos, " pat", info.pattern, " row", info.row, "\n")

        for ch in info.channel_info[:mod_info.chn]:
            print("*" if ch.event else " ", "I{:03d} #{:03d}".format(ch.instrument, ch.note), end="")
            volume = "#" * int((ch.volume / mod_info.gvl) * mod_info.vol_base / 2)
            print(" |", volume.ljust(mod_info.vol_base // 2, " "), "|")

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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("must give mod filename to play as argument")

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
