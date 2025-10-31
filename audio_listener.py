import sounddevice as sd
import numpy as np
import time
from collections import deque

class AudioListener:
    def __init__(self, config, executor, logger):
        self.config = config
        self.executor = executor
        self.logger = logger
        self.samplerate = config.get("samplerate", 44100)
        self.chunk = config.get("chunk_duration", 0.08)
        self.threshold = config.get("base_threshold", 0.28)
        self.cooldown = config.get("cooldown", 1.8)
        self.last_event = 0
        self.buffer = deque(maxlen=int(0.5 / self.chunk))

    def _bandpass(self, data):
        fft = np.fft.rfft(data)
        freqs = np.fft.rfftfreq(len(data), 1.0 / self.samplerate)
        mask = (freqs > 500) & (freqs < 6000)
        fft_filtered = fft * mask
        out = np.fft.irfft(fft_filtered)
        return out

    def _detect_claps_from_window(self, window):
        energy = np.linalg.norm(window)
        return energy

    def run(self):
        def callback(indata, frames, time_, status):
            mono = np.mean(indata, axis=1) if indata.ndim > 1 else indata[:, 0]
            filtered = self._bandpass(mono)
            energy = self._detect_claps_from_window(filtered)
            now = time.time()
            self.buffer.append((now, energy))
            peak = max(e for _, e in self.buffer)
            if peak > self.threshold and (now - self.last_event) > self.cooldown:
                times = [t for t, e in self.buffer if e > (self.threshold * 0.7)]
                if not times:
                    return
                groups = []
                current = [times[0]]
                for tt in times[1:]:
                    if tt - current[-1] < 0.45:
                        current.append(tt)
                    else:
                        groups.append(current)
                        current = [tt]
                groups.append(current)
                groups = sorted(groups, key=lambda g: len(g), reverse=True)
                count = len(groups[0]) if groups else 1
                self.logger.info("Clap group detected: %d", count)
                self.last_event = now
                if count == 1:
                    self.executor.execute_trigger("1_clap")
                elif count == 2:
                    self.executor.execute_trigger("2_claps")
                elif count >= 3:
                    self.executor.execute_trigger("3_claps")

        with sd.InputStream(callback=callback, channels=1, samplerate=self.samplerate, blocksize=int(self.samplerate * self.chunk)):
            while True:
                sd.sleep(1000)
