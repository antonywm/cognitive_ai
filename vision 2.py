############################################################################################################################
#   AZURE VISION AI DEMO - Antony Millington (c)2021 Resonate
#   vision2.py
#   This scripts takes an image from the command line (need to use explicit path to the file)
#   and analyses the image attributes. The image and its attributes are then displayed.
# 
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from python_code import vision

#  firstly we take the Endpoint and API Key from the Cognitive service we defined in Azure Portal:
cog_key = '2fc55b1b4c4e4a9ab1f1a80ba026dc03'
cog_endpoint = 'https://cog-vision-csdev.cognitiveservices.azure.com/'

#  Let's grab the name of the file we want to process from the command line:
image_path = input("Enter Filename: ")
image_path = image_path.replace("'","")

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# Specify the features we want to analyze
features = ['Description', 'Tags', 'Adult', 'Objects', 'Faces']

# Get an analysis from the computer vision service
image_stream = open(image_path, "rb")
analysis = computervision_client.analyze_image_in_stream(image_stream, visual_features=features)

# Show the results of analysis (code in helper_scripts/vision.py)
imgout = vision.show_image_analysis(image_path, analysis)


