import pyaudio

audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print(f"Device #{i}: {device_info['name']}")
    rates = [44100, 48000, 88200, 96000, 192000]
    for rate in rates:
        for channels in [1, 2]:
            try:
                if audio.is_format_supported(rate, input_device=device_info["index"], input_channels=channels, input_format=pyaudio.paInt16):
                    print(f"  {rate} Hz, {channels} channels: supported")
                else:
                    print(f"  {rate} Hz, {channels} channels: not supported")
            except ValueError:
                print(f"  {rate} Hz, {channels} channels: not supported")

audio.terminate()