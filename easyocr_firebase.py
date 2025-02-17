# -*- coding: utf-8 -*-
"""EasyOCR_Firebase

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GybJjQnCz_b7_q8i7qU8PBPS1DqSW_D5
"""
 
import cv2 
import easyocr
import firebase_admin
from firebase_admin import credentials 
from firebase_admin import db
import time

# Initialize OCR reader
print("Initializing OCR reader...")
reader = easyocr.Reader(['en'], gpu=False)
print("OCR reader initialized.")

# Set the path to the input image
image_path = '/content/WhatsApp Image 2023-07-03 at 5.42.52 PM.jpeg'

# Load the image
image = cv2.imread(image_path)

# Perform OCR on the image
try:
    print("Performing OCR on the image...")
    result = reader.readtext(image, detail=0)
    print("OCR completed.")
    print("Recognized text:")
    print(result)

    # Store recognized text
    recognized_text = result
except Exception as e:
    print("An error occurred during OCR processing:")
    print(str(e))
    recognized_text = []

# Determine the most frequent answer
final_text = recognized_text[0] if recognized_text else "No text detected"

print("Final predicted text:")
print(final_text)

# Initialize Firebase
cred = credentials.Certificate('/content/project1-7d2ef-firebase-adminsdk-a8avb-d8e1f13ae9.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project1-7d2ef-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the database
ref = db.reference()

# Set the current time
current_time = time.strftime('%Y-%m-%d %H:%M:%S')

# Store the data in the next row
new_row = {
    'Object_Detected': 'Nill',
    'Arrival_Time': current_time,
    'Cart_NO': final_text
}

# Push the new row to the database under "Station_02"
ref.child('Station_02').push(new_row)

# Close the Firebase app
firebase_admin.delete_app(firebase_admin.get_app())
