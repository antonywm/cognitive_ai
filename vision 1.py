############################################################################################################################
#   AZURE VISION AI DEMO - Antony Millington (c)2021 Resonate
#   vision1.py
#   This scripts takes an image from the command line (need to use explicit path to the file)
#   and analyses the image to create a caption. The caption and image are then displayed.
# 
import matplotlib.pyplot as plt
from PIL import Image

#  firstly we take the Endpoint and API Key from the Cognitive service we defined in Azure Portal:
cog_key = '2fc55b1b4c4e4a9ab1f1a80ba026dc03'
cog_endpoint = 'https://cog-vision-csdev.cognitiveservices.azure.com/'

#  Now we load the modules needed for the Vision service from Azure Cognitive Services:
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

#  Let's grab the name of the file we want to process from the command line:
image_path = input("Enter Filename: ")
image_path = image_path.replace("'","")
image_path = image_path.replace(" ","")

# Now we load a client for the computer vision service:
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# We can then call the service to get a description from computer vision
image_stream = open(image_path, "rb")
description = computervision_client.describe_image_in_stream(image_stream)

#  We are then just going to format it and display it on the screen
#  To do this, I use the Python Pillow library which is used for image processing
#  and Matplotlib which is a plotting library for Python (I use this to add a figure which creates an image and caption)
fig = plt.figure(figsize=(8, 8))
img = Image.open(image_path)
caption_text = ''
if (len(description.captions) == 0):
    caption_text = 'No caption detected'
else:
    for caption in description.captions:
        caption_text = caption_text + " '{}'\n(Confidence: {:.2f}%)".format(caption.text, caption.confidence * 100)
plt.title(caption_text)
plt.axis('off')
plt.imshow(img)
plt.show()