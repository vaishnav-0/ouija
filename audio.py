import tempfile
import wave

import numpy as np
import pyaudio
import torch
import whisper
from pyannote.audio import Pipeline


class Audio:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    def __init__(self, frame_rate=1, silent_frames=5):
        vad_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                use_auth_token="the key")
        vad_pipeline.to(torch.device("cuda"))

        model = whisper.load_model("small.en", device="cuda")

        self.vad_pipeline = vad_pipeline
        self.model = model
        self.frame_rate = 1 // frame_rate
        self.silent_frames = silent_frames

        self.audio = pyaudio.PyAudio()
        self.stream = self._get_stream()

        self.pre_recording = None
        self.post_recording = None
        self.while_silent = None

    def _get_stream(self):
        return self.audio.open(format=self.FORMAT,
                               channels=self.CHANNELS,
                               rate=self.RATE,
                               input=True,
                               frames_per_buffer=self.CHUNK)

    def _save_to_temp(self, frames):
        temp = tempfile.mktemp(suffix=".wav")
        with wave.open(temp, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        return temp

    def _record_and_detect_speech(self):
        """Record audio from the microphone and use VAD to detect end of speech."""

        self.stream.start_stream()

        frames = []
        speech_detected = False
        silence_counter = 0

        if self.pre_recording:
            self.pre_recording()

        while True:
            data = self.stream.read(int(self.RATE * self.frame_rate))
            frames.append(data)

            # Convert data to numpy array
            frame = np.frombuffer(data, dtype=np.int16)

            # Check for speech (reshape frame to match Pyannote's expected format)
            vad_result = self.vad_pipeline({
                "waveform": torch.tensor(frame, dtype=torch.float32).unsqueeze(0),
                "sample_rate": self.RATE
            })

            # Pyannote VAD returns an Annotation object where speech segments are marked
            is_speech = False
            for _ in vad_result.itertracks(yield_label=False):
                is_speech = True
                break

            if is_speech:
                speech_detected = True
                silence_counter = 0
            elif speech_detected:
                silence_counter += 1
                if silence_counter > self.silent_frames:
                    break

            if not is_speech and self.while_silent:
                self.while_silent(speech_detected)

        if self.post_recording:
            self.post_recording()

        self.stream.stop_stream()

        return self._save_to_temp(frames)

    def get_transcript(self):
        audio_file = self._record_and_detect_speech()
        result = self.model.transcribe(audio_file)

        return result["text"]

    def set_pre_recording(self, func):
        self.pre_recording = func

    def set_post_recording(self, func):
        self.post_recording = func

    def set_while_silent(self, func):
        self.while_silent = func


if __name__ == '__main__':
    audio = Audio(silent_frames=2)

    audio.set_pre_recording(lambda: print("Recording..."))
    audio.set_post_recording(lambda: print("Done recording"))
    audio.set_while_silent(lambda speech_detected: print("Silence" if not speech_detected else "Pause"))

    while True:
        print(audio.get_transcript())
