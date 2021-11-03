############################################################################################################################
#   AZURE VISION AI DEMO - Antony Millington (c)2021 Resonate
#   face 3.py
#   This matches faces with a group of learned faces
#     -  It requires a set of faces in a folder which are uploaded
# 
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from python_code import faces
import matplotlib.pyplot as plt
from PIL import Image
import os

cog_key = 'f0144c1b690847a4829bbd3abafb6f2e'
cog_endpoint = 'https://cog-multi-csdev.cognitiveservices.azure.com/'

# Create a face detection client.
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

group_id = 'resonate_employee_group_id'
try:
    # Delete group if it already exists
    face_client.person_group.delete(group_id)
except Exception as ex:
    print(ex.message)
finally:
    face_client.person_group.create(group_id, 'employees')
    print ('Group created: ' + group_id)

# Add a person to the group
empname = input("Enter Employee Name: ")
employee = face_client.person_group_person.create(group_id, empname)

# Get photo's of the employee
print ('Getting training images for employee: ' + empname)
folder = os.path.join('images', empname, 'training')
employee_pics = os.listdir(folder)
print (employee_pics)
# Register the photos
i = 0
fig = plt.figure(figsize=(8, 8))
for pic in employee_pics:
    # Add each photo to person in person group
    img_path = os.path.join(folder, pic)
    img_stream = open(img_path, "rb")
    face_client.person_group_person.add_face_from_stream(group_id, employee.person_id, img_stream)

    # Display each image
    img = Image.open(img_path)
    i +=1
    a=fig.add_subplot(1,len(employee_pics), i)
    a.axis('off')
    imgplot = plt.imshow(img)
print ('Created training group - close images to continue...')
plt.show()

# With the person added, and photographs registered, we can now train Face to recognize each person
print('Training....')
face_client.person_group.train(group_id)
print('Trained!')

# Get the face IDs in a second image
#  Let's grab the name of the file we want to process from the command line:
image_path = input("Enter Facial Recognition Test Filename: ")
while image_path != "":
    image_path = image_path.replace("'","")
    image_stream = open(image_path, "rb")
    image_faces = face_client.face.detect_with_stream(image=image_stream)
    image_face_ids = list(map(lambda face: face.face_id, image_faces))

    # Get recognized face names
    face_names = {}
    recognized_faces = face_client.face.identify(image_face_ids, group_id)
    if not recognized_faces:
        print('No Face')
    else:
        for face in recognized_faces:
            try:
                person_name = face_client.person_group_person.get(group_id, face.candidates[0].person_id).name
                face_names[face.face_id] = person_name
            except:
                pass
        # show recognized faces
        faces.show_recognized_faces(image_path, image_faces, face_names)
        plt.show()
    image_path = input("Enter Filename: ")