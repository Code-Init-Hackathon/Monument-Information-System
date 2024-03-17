import os
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

SCRAPED_DATA_DIRECTORY = "scraped_content"
PHOTO_STORAGE_FIREBASE_DIRECTORY = "photos"
LOGS_DIRECTORY = "logs"
UPPER_LIMIT = 30

if LOGS_DIRECTORY not in os.listdir():
    os.mkdir(LOGS_DIRECTORY)

cred = credentials.Certificate("firebase_credentials.json")

firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client(app = firebase_app)
storage_client = storage.bucket(name = 'monument-information-system.appspot.com',app = firebase_app)

WEBSCRAPING_FILE = "webscraping.py"

def scrape_data():
    subprocess.run(['python3',WEBSCRAPING_FILE])
    print("=> [Finished Scraping Data]")

def preprocess_data_to_firebase():
    f = open(os.path.join(LOGS_DIRECTORY,"scraped_content_log.txt"),"wt")
    f.close()
    files_completed = 0
    for number,folder in enumerate(os.listdir(SCRAPED_DATA_DIRECTORY)):
        if(number >= UPPER_LIMIT):
            break
        files = os.listdir(os.path.join(SCRAPED_DATA_DIRECTORY,folder))

        all_files_present = True
        for file in [f"{folder}.jpg","description.txt","coordinates.txt"]:
            if file not in files:
                all_files_present = False
                with open(os.path.join(LOGS_DIRECTORY,"scraped_content_log.txt"),"at") as f:
                    f.write(f"{file} could not be found in {SCRAPED_DATA_DIRECTORY} folder.\n")

        if(all_files_present == False):
            continue    
        photo_filename = os.path.join(SCRAPED_DATA_DIRECTORY,folder,f"{folder}.jpg")


        with open(os.path.join(SCRAPED_DATA_DIRECTORY,folder,"coordinates.txt"),"rt") as f:
            latitude = f.readline()
            longitude = f.readline()

        with open(os.path.join(SCRAPED_DATA_DIRECTORY,folder,"description.txt"),"rt") as f:
            description = f.read()

        doc_ref = db.collection("monuments").document(folder)
        content = {
            'Name' : folder,
            'Coordinates' : f"{latitude} \n{longitude}",
            'Description' : description
        }
        doc_ref.set(content)

        blob = storage_client.blob(f"{PHOTO_STORAGE_FIREBASE_DIRECTORY}/{folder}.jpg")
        blob.upload_from_filename(photo_filename)
        files_completed += 1
    print(f"=> [{files_completed} have been processed and uploaded to firebase]")

scrape_data()
preprocess_data_to_firebase()
