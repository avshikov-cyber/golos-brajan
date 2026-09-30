import torch
import numpy as np
from silero_vad import load_silero_vad, VADIterator

class VoiceProcessor:
    def __init__(self, sample_rate=16000, threshold=0.5, min_silence_ms=500):
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.min_silence_ms = min_silence_ms
        self.vad_model = load_silero_vad()
        self.vad_iterator = VADIterator(
            self.vad_model,
            threshold=self.threshold,
            sampling_rate=self.sample_rate,
            min_silence_duration_ms=self.min_silence_ms
        )
        self.audio_buffer = []
        self.is_speaking = False

    def process_chunk(self, audio_bytes):
        # Преобразуем int16 -> float32
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_float32 = audio_int16.astype(np.float32) / 32768.0
        
        # --- РАЗБИВАЕМ НА КУСКИ ПО 512 СЭМПЛОВ ---
        chunk_size = 512
        for i in range(0, len(audio_float32), chunk_size):
            chunk = audio_float32[i:i+chunk_size]
            if len(chunk) < chunk_size:
                # Добиваем нулями до 512, если кусок меньше
                chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
            
            audio_tensor = torch.from_numpy(chunk).unsqueeze(0)
            
            # Передаём в VAD
            speech_dict = self.vad_iterator(audio_tensor, return_seconds=False)
            
            if speech_dict:
                self.audio_buffer.append(audio_tensor)
                self.is_speaking = True
            elif self.audio_buffer:
                # Речь закончилась — собираем всё
                full_audio = torch.cat(self.audio_buffer, dim=1)
                self.audio_buffer.clear()
                self.is_speaking = False
                return full_audio, True
        
        return None, False

    def reset(self):
        self.audio_buffer.clear()
        self.is_speaking = False
        self.vad_iterator.reset_states()