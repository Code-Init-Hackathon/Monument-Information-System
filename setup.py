import os
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SCRAPED_DATA_DIRECTORY = os.path.join(CURRENT_DIRECTORY,"scraped_content")
PHOTO_STORAGE_FIREBASE_DIRECTORY = "photos"

cred = credentials.Certificate("firebase_credentials.json")

firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client(app = firebase_app)
storage_client = storage.bucket(name = 'monument-information-system.appspot.com',app = firebase_app)

WEBSCRAPING_FILE = "webscraping.py"

def scrape_data():
    subprocess.run(['python3',WEBSCRAPING_FILE])

def preprocess_data_to_firebase():
    for file in os.listdir(SCRAPED_DATA_DIRECTORY):
        photo_filename = os.path.join(SCRAPED_DATA_DIRECTORY,f"{file}",f"{file}.jpg")
        with open(os.path.join(SCRAPED_DATA_DIRECTORY,f"{file}","coordinates.txt"),"rt") as f:
            latitude = f.readline()
            longitude = f.readline()
        with open(os.path.join(SCRAPED_DATA_DIRECTORY,f"{file}","description.txt"),"rt") as f:
            description = f.read()

        doc_ref = db.collection("monuments").document(file)
        content = {
            'Name' : file,
            'Coordinates' : f"{latitude} \n{longitude}",
            'Description' : description
        }
        doc_ref.set(content)

        blob = storage_client.blob(f"{PHOTO_STORAGE_FIREBASE_DIRECTORY}/{file}.jpg")
        blob.upload_from_filename(photo_filename)
scrape_data()
preprocess_data_to_firebase()
