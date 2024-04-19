# import serial
# import time
# import requests

# # Configure serial port
# ser = serial.Serial('/dev/ttyUSB0', 9600)

# def store_fingerprint_in_database(hand, finger, fingerprint_image):
#     # Assuming Django server is running locally
#     url = 'http://localhost:8000/store_fingerprint/'
#     data = {
#         'hand': hand,
#         'finger': finger,
#         'fingerprint_image': fingerprint_image,
#     }
#     response = requests.post(url, data=data)
#     if response.status_code == 200:
#         print("Fingerprint stored successfully.")
#     else:
#         print("Failed to store fingerprint.")

# while True:
#     if ser.in_waiting > 0:
#         data = ser.readline().decode().strip()
#         hand, finger, fingerprint_image = data.split(',')
#         store_fingerprint_in_database(hand, finger, fingerprint_image)