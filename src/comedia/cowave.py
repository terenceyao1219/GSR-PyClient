import os
from . import wave

class CoWave:
    n_channels = 0
    sample_width = 0
    sample_rate = 0
    n_frames = 0
    compression_type = 'unk'
    compression_name = 'Unknown'
    audio_bytes: bytes = None

    def __init__(self, filename: str):
        if not os.path.exists(filename):
            return
        wave_file = wave.open(filename, 'rb')
        self.n_channels = wave_file.getnchannels()
        self.sample_width = wave_file.getsampwidth()
        self.sample_rate = wave_file.getframerate()
        self.n_frames = wave_file.getnframes()
        self.compression_type = wave_file.getcomptype()
        self.compression_name = wave_file.getcompname()
        self.audio_bytes = wave_file.readframes(self.n_frames)
        wave_file.close()

    def get_info_name(self) -> str:
        c_type = self.compression_type.lower()
        if c_type == 'none':
            c_type = 'pcm'
        return f'ch{self.n_channels}-{self.sample_rate}-{c_type}'

    def get_chunks(self, chunk_size=512) -> list[bytes]:
        if self.audio_bytes is None:
            return []
        if chunk_size <= 8:
            chunk_size = 8
        data = self.audio_bytes
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    def print_info(self):
        print("Info Name        :", self.get_info_name())
        print("Sample Width     :", self.sample_width)
        print("Sample Rate      :", self.sample_rate, 'Hz')
        print("Channel          :", self.n_channels)
        print("Frames           :", self.n_frames)
        print("Compression Type :", self.compression_type)
        print("Compression Name :", self.compression_name)
        print("Data Length      :", len(self.audio_bytes))

    def is_valid(self) -> bool:
        return self.audio_bytes is not None