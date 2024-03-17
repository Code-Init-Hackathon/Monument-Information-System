import os
import sys 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

PHOTO_STORAGE_FIREBASE_DIRECTORY = "photos"

cred = credentials.Certificate("firebase_credentials.json")

firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client(app = firebase_app)
storage_client = storage.bucket(name = "monument-information-system.appspot.com",app = firebase_app)

LOCAL_DATABASE_FOLDER = sys.argv[1]
NAME = sys.argv[2]
PHOTO_FILE_PATH = sys.argv[3]
REQUIRED_FOLDER = os.path.join(LOCAL_DATABASE_FOLDER,NAME)

description = ""
coordinates = ""

if "coordinates.txt" in os.listdir(REQUIRED_FOLDER):
    with open(os.path.join(REQUIRED_FOLDER,"coordinates.txt"),"rt") as f:
        coordinates = f.read()
if "description.txt" in os.listdir(REQUIRED_FOLDER):
    with open(os.path.join(REQUIRED_FOLDER,"description.txt"),"rt") as f:
        description = f.read()


doc_ref = db.collection("monuments").document(NAME)        
content = {
    'Name' : NAME,
    'Coordinates' : coordinates,
    'Description' : description
}
doc_ref.set(content)

blob = storage_client.blob(f"{PHOTO_STORAGE_FIREBASE_DIRECTORY}/{NAME}.jpg")
blob.upload_from_filename(PHOTO_FILE_PATH)