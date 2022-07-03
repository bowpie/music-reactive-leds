from audiostream import AudioStream
from arduinoserial import ArduinoSerial
from rgbcolor import RgbColor
from config import *
from time import sleep as delay
import keyboard as kb
import logging
import atexit


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def generate_range(min_amp, max_amp, count, **kwargs):
    try:
        assert max_amp - min_amp >= count, "Amps are equal"
    except:
        max_amp = min_amp + count

    step = (max_amp - min_amp + 1) // count
    ranges = [(i, i + step) for i in range(min_amp, min_amp + step * count, step)]
    return ranges


def generate_colors(reactive: bool = True, color_names: list = [], **kwargs: dict):
    if reactive:
        hue_min = kwargs.get("hue_min", 0)
        hue_max = kwargs.get("hue_max", 280)
        step = (hue_max - hue_min + 1) // kwargs.get("count", 10)
        return [RgbColor(hsv=(hue, 1, 1)) for hue in range(hue_min, hue_max, step)][
            ::-1
        ]
    else:
        return [RgbColor(name=name) for name in color_names]


def generate_color_range():
    colors = generate_colors(
        reactive=REACTIVE, color_names=COLOR_NAMES, count=REACTIVE_COUNT
    )
    ranges = list(range(*FREQ_RANGE, (FREQ_RANGE[1] - FREQ_RANGE[0]) // len(colors)))
    return [(ranges[i], colors[i]) for i in range(len(colors))]


def search_range(freq, color_ranges: list):
    for i, x in list(enumerate(color_ranges))[::-1]:
        if freq > x[0]:
            return x
    return color_ranges[0]


def generate_power(db, db_range: tuple):
    return map_range(db, *db_range, 0, 100)


def handle_exit(audio, serial):
    serial.communicate((0, 0, 0))
    audio.stop_stream()
    serial.stop_serial()


def main_loop(audio, serial, color_ranges):
    running = True

    while running:
        freq, db = audio.get_current_freq()

        if freq:
            power = generate_power(db, db_range=DB_RANGE)
            frange, color = search_range(freq, color_ranges)

            color = color.power(power)

            serial.communicate(color.rgb)

            # printer = {
            #     "freq": freq,
            #     "note": AudioStream.pitch(freq)[0],
            #     "power": round(power, 2),
            #     "db": db,
            #     "color": color.__str__(),
            # }
            # print(f"{50*'-'}\n", json.dumps(printer, indent=4), f"{50*'-'}\n")
            # delay(0.01)

        try:
            if kb.is_pressed(STOP_KEY):
                exit()
        except KeyboardInterrupt:
            exit()


def main():
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    audio = AudioStream(
        chunk=CHUNK,
        channel=CHANNEL,
        rate=RATE,
        device_index=DEVICE_INDEX,
        freq_bounds=FREQ_RANGE,
        threshold=DB_THRESHOLD,
    )
    serial = ArduinoSerial(port=ARDUINO_PORT, debug=DEBUG_MODE)

    serial.start_serial()
    # a nice power on animation
    serial.communicate((0, 0, 0))
    delay(0.5)
    serial.communicate((255, 255, 255))
    delay(0.5)
    serial.communicate((0, 0, 0))

    # audio.enum_devices()
    audio.start_stream()

    atexit.register(handle_exit, audio, serial)

    main_loop(audio, serial, generate_color_range())


if __name__ == "__main__":
    main()
