# Music Reactive RGB LEDs using Pyaudio

---

> A script written in Python 3.8 with pyaudio to analyze and process an audio stream in real-time, map every frequency to a color and then send an rgb code to an arduino to control the rgb led strap.

## Description

---

I've used `Voicemeeter Banana`, an audio mixer endowed with a Virtual Audio Device to redirect the speaker output sound to a virtual input device that could be used by Pyaudio.

The processing of the raw data was made using Fast Fourier Transform algorithms (FFT) and signal processing techniques such as windowing, filtering and interpolating. For that I've used two popular python modules: `numpy` and `scipy`.

To map colors to frequencies I've divided both the frequency range and a hue range into a number of portions(`REACTIVE_COUNT`) and then associated them with one another.

The controller consists of an arduino and a circuit that looks like the one below (classic rgb led controller circuit from the internet).

![Circuit Board](/screenshots/arduinocircuit.png)

## Getting started

---

### Dependencies

- The following Python 3.8.4 modules: pyaudio, numpy, scipy, serial

```
cd ./python
pip install -r requirements.txt
```

### Usage

After building a circuit similar to the one above and modifying the pins inside the arduino program acording to your build, you need to configure a Virtual Audio Device like Voicemeeter Banana and then modify `config.py`.

Finally you need to run `main.py`:

```
cd /python
py ./main.py
```

### Demo

You can see how the script works with different songs:

#### https://youtu.be/lhvDzmtW1C0

## License

---

This project is licensed under the MIT License - see the LICENSE.md file for details.
