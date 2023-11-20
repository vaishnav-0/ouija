import os
import tempfile
import pyaudio
import wave
import whisper
from pyannote.audio import Pipeline
import torch


def record_and_detect_speech(vad_pipeline):
    """Record audio from the microphone and use VAD to detect end of speech."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    speech_detected = False
    silence_counter = 0

    print("* recording")

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Check for speech
        is_speech = vad_pipeline(
            {"waveform": torch.tensor(wave.struct.unpack("%dh" % (len(data) // 2), data), dtype=torch.float32),
             "sample_rate": RATE}).get("speech")

        if is_speech:
            speech_detected = True
            silence_counter = 0
        elif speech_detected:
            silence_counter += 1
            if silence_counter > 20:  # Adjust as needed
                break

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save to temporary file
    WAVE_OUTPUT_FILENAME = tempfile.mktemp(suffix=".wav")
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return WAVE_OUTPUT_FILENAME


def transcribe_audio(model, file_path):
    """Transcribe the audio file using Whisper."""
    result = model.transcribe(file_path)
    return result["text"]


def speech_to_text_generator():
    vad_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                            use_auth_token="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")
    vad_pipeline.to(torch.device("cuda"))

    model = whisper.load_model("small.en", device="cuda")

    while True:
        print("Please speak...")

        # Record the speech and detect the end of speech
        audio_file = record_and_detect_speech(vad_pipeline)

        # Transcribe using Whisper
        try:
            sentence = transcribe_audio(model, audio_file)
            yield sentence
        finally:
            # Clean up the temporary audio file
            os.remove(audio_file)


# Using the generator
generator = speech_to_text_generator()
for _ in range(3):  # Example: getting 3 sentences
    print(next(generator))
