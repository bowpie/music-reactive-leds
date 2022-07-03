# Path for the list of colors
COLORS_PATH = "color_dict.json"
# (min, max) allowed Frequencies
FREQ_RANGE = (20, 1200)
# (min, max) allowed Decibels
DB_RANGE = (85, 120)
# No. of samples of audio data we analyze at a time (for the FFT)
CHUNK = 1024 * 3
# Channels - recommended 1
CHANNEL = 1
# Rate of the audio, in Hz
RATE = 48000
# Threshold to filter out the unhearable noise
DB_THRESHOLD = 30
# Device index, you can get it by calling enum_devices()
DEVICE_INDEX = 4
# USB port for the arduino connection
ARDUINO_PORT = "COM5"
# If DEBUG_MODE = True, arduino won't receive the commands
DEBUG_MODE = False
# Reactive = False, you can choose what colors you want from the list of colors
# Reactive = True, REACTIVE_COUNT number of colors are generated automatically
REACTIVE = True
# List of colors from color_dict.json, ONLY IF REACTIVE = FALSE
COLOR_NAMES = ["dark_red"]
# Number of colors to generate automatically, ONLY IF REACTIVE = TRUE
REACTIVE_COUNT = 10
# Key or combination of keys to stop running the loop, ctrl+c also works
STOP_KEY = "ctrl+k"
