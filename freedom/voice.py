# import requests
# import base64
# import pygame
# import io
# import time

# # Initialize Pygame mixer
# pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
# access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJTaGl2YW4iLCJhY2NvdW50X3R5cGUiOiJGcmVlIiwiZXhwIjo0ODYyMjI0MDk1fQ.9wIrzuZIM6qj7BLtfvwb70TjwTq81njGkZaeUr49-_E'  # Replace with your actual access token

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# payload = {
#     "text": "Oli otya?"
# }
# response = requests.post(f"{url}/tasks/tts", headers=headers, json=payload)

# if response.status_code == 200:
#     base64_string = response.json()["base64_string"]
    
#     # Decode base64 string to bytes
#     decoded_audio = base64.decodebytes(base64_string.encode('utf-8'))
    
#     # Create a BytesIO object to load the audio data
#     audio_stream = io.BytesIO(decoded_audio)

#     # Load the audio stream into Pygame mixer
#     pygame.mixer.music.load(audio_stream)
    
#     # Play the audio
#     pygame.mixer.music.play()

#     # Wait for the audio to finish playing
#     #pygame.time.wait(int(pygame.mixer.music.get_pos()))
#     # Wait for the audio to finish playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(30)  # Adjust the clock speed if needed
# else:
#     print("Error:", response.status_code, response.text)
