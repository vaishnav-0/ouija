import os
import queue
import sys
import pyaudio
from vosk import Model, KaldiRecognizer

model = Model(lang="en")

# Initialize PyAudio
q = queue.Queue()
audio_interface = pyaudio.PyAudio()
stream = audio_interface.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


# Function to process microphone input
def process_audio(in_data, frame_count, time_info, status_flags):
    q.put(in_data)
    return None, pyaudio.paContinue


# Start the audio stream
audio_interface.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000,
                     stream_callback=process_audio)

# Create a recognizer object
recognizer = KaldiRecognizer(model, 16000)

while True:
    data = q.get()
    if recognizer.AcceptWaveform(data):
        print(recognizer.Result())
    else:
        print(recognizer.PartialResult())

# Stop and close the stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio
audio_interface.terminate()
