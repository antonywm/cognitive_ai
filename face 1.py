############################################################################################################################
#   AZURE VISION AI DEMO - Antony Millington (c)2021
#   face 1.py
#   This finds faces in an image and draws a bounding box around the face
#
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# This is the endpoint URL and API key from our Azure service:
ENDPOINT = "https://cog-face-csdev.cognitiveservices.azure.com/"
KEY = "9a75f02a798b473f9aafed356880de66"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

#  Let's grab the name of the file we want to process from the command line:
image_path = input("Enter Filename: ")
image_path = image_path.replace("'","")
image_data = open(image_path, "rb")

# We use detection model 3 (February 2021) to get better performance.
detected_faces = face_client.face.detect_with_stream(image=image_data, detection_model='detection_03')
if not detected_faces:
    raise Exception('No face detected from image {}'.format(image_path))

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    return ((left, top), (right, bottom))

# For each face returned use the face rectangle and draw a red box.
print('Drawing rectangle around face... see popup for results.')
img = Image.open(image_path)
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline='red')

# Display the image in the users default image browser.
img.show()
