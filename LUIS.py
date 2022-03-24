############################################################################################################################
#   AZURE LUIS AI DEMO - Antony Millington (c)2021
#   LUIS.py
#   This provides a prompt for user input. Passes it to LUIS for language analysis and then pushes the result to a power
#   automate flow to process the action
# 
from python_code import luis
import matplotlib.pyplot as plt
from PIL import Image
import os
import requests

try:
    # Set up API configuration
    luis_app_id = '3f93014a-b125-4526-acdd-1d1e404c2d36'
    luis_key = 'f0144c1b690847a4829bbd3abafb6f2e'
    luis_endpoint = 'https://cog-multi-csdev.cognitiveservices.azure.com/'

    # prompt for a command
    command = input('Please enter a command: \n')

    print('Sending to LUIS:')
    # get the predicted intent and entity (code in python_code.home_auto.py)
    action = luis.get_intent(luis_app_id, luis_key, luis_endpoint, command)

    # trigger flow
    print('Triggering Flow:')
    r = requests.post('https://prod-175.westeurope.logic.azure.com:443/workflows/4233738199204a5b868f7c38929ac588/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=iWSll0Cy0J5Mzp28EOB3IN4yNJ6hfaV8eb80cGDcy8w')
    print('Flow trigger return code: ', r.status_code)
except Exception as ex:
    print(ex)
