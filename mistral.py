import numpy as np
from litellm import completion
# from litellm import completion
from transformers import WhisperProcessor, WhisperForConditionalGeneration
# from datasets import load_dataset
import pyaudio
import soundfile as sf


# processor = WhisperProcessor.from_pretrained("openai/whisper-large", cache_dir="huggingface")
#
# model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large", cache_dir="huggingface")
#

p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
#
# samplerates = 32000, 44100, 48000, 96000, 128000
#
# for i in range(0, numdevices):
#     devinfo = p.get_device_info_by_index(i)
#     if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#         print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
#         print(devinfo)
#         for fs in samplerates:
#             try:
#                 p.is_format_supported(fs,  # Sample rate
#                                       input_device=devinfo['index'],
#                                       input_channels=devinfo['maxInputChannels'],
#                                       input_format=pyaudio.paInt16)
#             except Exception as e:
#                 print(fs, e)
#             else:
#                 print(fs, 'ok')
# Or whatever device you care about.

DEVICE_IDX = 7
FORMAT = pyaudio.paInt16  # Format for audio samples (16-bit)
CHANNELS = 2  # Mono audio
RATE = 48000  # Sample rate (samples per second)
RECORD_SECONDS = 2  # Duration of recording in seconds
CHUNK = 2048

out = np.array([], dtype="int16")

# Initialize the audio stream
audio = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    global out
    out = np.append(out, np.fromstring(in_data, dtype=np.float32).astype(np.float32))
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
    print(out)
    # resampled_audio = librosa.resample(out, orig_sr=RATE, target_sr=16000)
    #
    # input_features = processor(resampled_audio, sampling_rate=16000,
    #                            return_tensors="pt").input_features
    # #
    # # # generate token ids
    # predicted_ids = model.generate(input_features)
    # # # decode token ids to text
    # transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
    # #
    # #
    # # transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    # #
    # print(transcription)
    output_file = "output.wav"

    # Save the NumPy array as a WAV file using Librosa
    sf.write(output_file, out, 48000)
    quit()




# ds = load_dataset("whisper/librispeech_dummy.py", "clean", split="validation")
# sample = ds[0]["audio"]

# generate token ids
# decode token ids to text


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
