############################################################################################################################
#   AZURE VISION AI DEMO - Antony Millington (c)2021 Resonate
#   face 2.py
#   This finds faces in an image and extracts facial attributes from the image
#
from azure.cognitiveservices.vision.face import FaceClient
from matplotlib.pyplot import waitforbuttonpress
from msrest.authentication import CognitiveServicesCredentials
from python_code import faces
import os

# This is the endpoint URL and API key from our Azure service:
ENDPOINT = "https://cog-face-csdev.cognitiveservices.azure.com/"
KEY = "9a75f02a798b473f9aafed356880de66"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

#  Let's grab the name of the file we want to process from the command line:
image_path = input("Enter Filename: ")
image_path = image_path.replace("'","")
image_stream = open(image_path, "rb")

# Detect faces and specified facial attributes
attributes = ['age', 'emotion']
detected_faces = face_client.face.detect_with_stream(image=image_stream, return_face_attributes=attributes)

# Display the faces and attributes (code in python_code/faces.py)'/Users/antony/vscode/AI900/images/ResonateMeetTheTeam.jpg'
faces.show_face_attributes(image_path, detected_faces)
waitforbuttonpress()
