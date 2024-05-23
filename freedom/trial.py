import pyaudio, wave
import os
import sys

sys.stderr = open(os.devnull, 'w')


def record_audio(duration, fs=48000):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = fs
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "test_voice.wav"
    DEVICE_INDEX = 2
    # Initialize the audio stream
    audio = pyaudio.PyAudio()
    # Open the audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)
    print("Recording started...")
    # Create a buffer to store the recorded audio frames
    frames = []
    # Record audio for the specified duration
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")
    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # Save the recorded audio to a WAV file
    wave_file = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
    return WAVE_OUTPUT_FILENAME

audio_file = record_audio(10)
print("Audio file saved as", audio_file)