import time
import librosa
import wave
import numpy as np
from litellm import completion
import whisper
import pyaudio


p = pyaudio.PyAudio()


DEVICE_IDX = 7
FORMAT = pyaudio.paInt16  # Format for audio samples (16-bit)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate (samples per second)
RECORD_SECONDS = 2  # Duration of recording in seconds
CHUNK = 1024*4

out = np.array([], dtype="float32")

# Initialize the audio stream
audio = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    global out
    out = np.append(out, np.nan_to_num(np.fromstring(in_data, dtype=np.float32)))
    return in_data, pyaudio.paContinue


stream = audio.open(format=FORMAT, channels=CHANNELS, input_device_index=DEVICE_IDX,
                    rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)

print("Recording...")

stream.start_stream()

# Record audio for the specified duration
frames = []

try:

    while True:
        pass

except KeyboardInterrupt:

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("* Killed Process")
    output_file = "output.wav"

    # resampled_audio = librosa.resample(out, orig_sr=RATE, target_sr=16000, fix=True)
    #
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(44100)
        wf.writeframes(out.tobytes())
    print(out)

    model = whisper.load_model("small", download_root="whisper")
    result = model.transcribe("output.wav", language="en")

    print(result["text"])

    quit()




# transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
#
# response = completion(
#     model="ollama/mistral",
#     messages=[{"content": "You are Alan Mathison Turing the english computer scientist. YOu are profane. respond in maximum 2 words. Never role play", "role": "system"},
#               {"content": "Teach me some cuss words. ", "role": "user"}
#               ],
#     api_base="http://localhost:11434"
# )
#
# print(response)
