############################################################################################################################
#   AZURE TEXT ANALYSIS AI DEMO - Antony Millington (c)2021 Resonate
#   ocr.py
#   This analyses an image with signage or lettering/numbering within the image and converts into ASCII text, displayed on
#   the command line
# 
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

cog_key = 'f0144c1b690847a4829bbd3abafb6f2e'
cog_endpoint = 'https://cog-multi-csdev.cognitiveservices.azure.com/'

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# Read the image file
image_path = os.path.join('images', 'ocr', 'resonate-webinar.jpeg')
image_stream = open(image_path, "rb")

# Use the Computer Vision service to find text in the image
read_results = computervision_client.recognize_printed_text_in_stream(image_stream)

# Process the text line by line
for region in read_results.regions:
    for line in region.lines:

        # Read the words in the line of text
        line_text = ''
        for word in line.words:
            line_text += word.text + ' '
        print(line_text.rstrip())

# Open image to display it
fig = plt.figure(figsize=(7, 7))
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Process the text line by line
for region in read_results.regions:
    for line in region.lines:

        # Show the position of the line of text
        l,t,w,h = list(map(int, line.bounding_box.split(',')))
        draw.rectangle(((l,t), (l+w, t+h)), outline='magenta', width=5)

        # Read the words in the line of text
        line_text = ''
        for word in line.words:
            line_text += word.text + ' '
        print(line_text.rstrip())

# Show the image with the text locations highlighted
plt.axis('off')
plt.imshow(img)
plt.waitforbuttonpress()
