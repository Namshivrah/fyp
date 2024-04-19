import requests
import pyaudio
import wave

<<<<<<< HEAD

=======
>>>>>>> 3409599e8033f19433aae308b612cf1988cd5850
# missing key

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    response=response.json()
    if "text" not in response:
        return response['error']
    return response['text']

def record_audio():
    # Code to record audio and save it as a WAV file
    # You can use libraries like pyaudio or sounddevice to handle audio recording

    # Example using pyaudio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3
    filename = "audio_file.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return filename

# Example usage
# audio_file = 'E:/Voting django/voting/static/responses/responses.wav' # Path to the audio file
# record_audio(audio_file)

output = query(record_audio())
print(output)

import sounddevice as sd

def print_microphones():
    microphones = sd.query_devices()
    print("Connected microphones:")
    for idx, device in enumerate(microphones):
        if 'input' in device['name'].lower():
            print(f"{idx + 1}. {device['name']}")

# print_microphones()