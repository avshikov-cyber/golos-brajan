import pyaudio
import numpy as np

CHUNK = 4000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)

print("🎤 Говори что-нибудь... (Ctrl+C для выхода)")
try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
        if rms > 0.01:
            print(f"🔊 Слышу! RMS: {rms:.4f}")
        else:
            print(".", end="", flush=True)
except KeyboardInterrupt:
    print("\n👋 Выход")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()