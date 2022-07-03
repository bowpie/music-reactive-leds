import pyaudio
import numpy as np
from scipy.interpolate import interp1d
from math import log2
import logging


class AudioStream:
    logger = logging.getLogger(__name__)

    def __init__(
        self,
        chunk,
        channel,
        rate,
        device_index,
        format=pyaudio.paInt16,
        freq_bounds=(80, 1200),
        threshold=30,
    ):
        self._chunk = chunk
        self._format = format
        self._channel = channel
        self._rate = rate
        self._device_index = device_index
        self._min_freq, self._max_freq = freq_bounds
        self._main_freq = self._main_db = 0
        self._threshold = threshold
        self._pyaudio_obj = pyaudio.PyAudio()

    def start_stream(self):
        self.stream = self._pyaudio_obj.open(
            format=self._format,
            channels=self._channel,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            input_device_index=self._device_index,
            stream_callback=self._procces_stream,
        )

        self.stream.start_stream()
        AudioStream.logger.info("Audio stream has opened. * Started recording.")

    def _calculate_freq_db(self, data, db_constant=120):
        # https://dsp.stackexchange.com/questions/32076/fft-to-spectrum-in-decibel
        win = np.kaiser(len(data), 14)  # window
        ref = 32768  # ref: reference value used for dBFS scale. 32768 for int16 and 1 for float

        data = data * win
        sp = np.abs(np.fft.rfft(data))  # sp means spectrum
        freq = np.fft.rfftfreq(self._chunk, 1 / self._rate)
        s_mag = np.abs(sp) * 2 / np.sum(win)
        s_dbfs = 20 * np.log10(s_mag / ref)
        db = s_dbfs + db_constant
        # fftTime=np.fft.rfftfreq(self.chunk, 1./self.rate)
        return freq, db

    @staticmethod
    def _interpolate_around_max(freq, db, around=1):
        # around = range around max, how many points to take around the maximum frequency
        # interpolate around x1 and x2
        # returns max freq and max db after interpolation
        interp_func = interp1d(freq, db, kind="quadratic")
        argmax = np.argmax(db)
        if argmax + around > len(freq) - 1:
            x1, x2 = freq[argmax - around], freq[argmax]
        elif argmax - around + 1 <= 0:
            x1, x2 = freq[argmax], freq[argmax + around]
        else:
            x1, x2 = freq[argmax - around], freq[argmax + around]

        xnew = np.arange(x1, x2, 0.1)
        ynew = interp_func(xnew)
        new_arg = np.argmax(ynew)
        return (xnew[new_arg], ynew[new_arg])

    def _procces_stream(self, in_data, frame_count, time_info, status_flag):
        data = np.frombuffer(in_data, dtype=np.int16)
        freqs, db = self._calculate_freq_db(data)
        self._main_freq, self._main_db = self._interpolate_around_max(freqs, db, 1)
        AudioStream.constrain(self._main_freq, self._min_freq, self._max_freq)

        if self._main_db < self._threshold:
            self._main_freq = self._main_db = 0

        return (in_data, pyaudio.paContinue)

    def get_current_freq(self):
        return (round(self._main_freq, 2), int(self._main_db))

    def stop_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        AudioStream.logger.info("Audio stream has closed. * Stopped recording.")

    def enum_devices(self):
        for i in range(self._pyaudio_obj.get_device_count()):
            print(
                i,
                self._pyaudio_obj.get_device_info_by_index(i)["name"],
                self._pyaudio_obj.get_device_info_by_index(i)["maxInputChannels"],
            )

    @staticmethod
    def pitch(freq):
        A4 = 440
        C0 = A4 * pow(2, -4.75)
        name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        h = round(12 * log2(freq / C0))
        octave = h // 12
        n = h % 12
        return (name[n], str(octave))

    @staticmethod
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))
