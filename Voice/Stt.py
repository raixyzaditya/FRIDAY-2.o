import os
import queue
import tempfile

import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
import whisper

from Config import WHISPER_MODEL, SAMPLE_RATE

print(
    f"For Speech to text conversion, we are loading whisper {WHISPER_MODEL} model...",
    end="",
    flush=True
)

MODEL = whisper.load_model(WHISPER_MODEL)

print("Done")



def record_audio(
    sample_rate=SAMPLE_RATE,
    silence_threshold=500,
    silence_duration=1.2,
    max_duration=10
):

    print("[STT] Listening...")

    q = queue.Queue()

    audio_chunks = []

    silence_chunks = 0

    chunk_duration = 0.2
    chunk_samples = int(sample_rate * chunk_duration)

    max_chunks = int(max_duration / chunk_duration)

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        blocksize=chunk_samples,
        callback=callback
    ):

        started = False

        for _ in range(max_chunks):

            chunk = q.get()

            volume = np.abs(chunk).mean()

            if volume > silence_threshold:
                started = True
                silence_chunks = 0
            else:
                if started:
                    silence_chunks += 1

            if started:
                audio_chunks.append(chunk)

            
            if silence_chunks > silence_duration / chunk_duration:
                break

    print("[STT] Recording complete")

    if len(audio_chunks) == 0:
        return np.array([], dtype=np.int16)

    audio = np.concatenate(audio_chunks, axis=0)

    return audio.flatten()



def save_wave(audio, sample_rate=SAMPLE_RATE):

    temp = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    wav.write(temp.name, sample_rate, audio)

    return temp.name



def transcribe(wav_path):

    result = MODEL.transcribe(wav_path)

    return result["text"].strip()



def record_and_transcribe():

    audio = record_audio()

    if len(audio) == 0:
        return ""

    wav_path = save_wave(audio)

    try:
        text = transcribe(wav_path)

    finally:
        os.remove(wav_path)

    return text