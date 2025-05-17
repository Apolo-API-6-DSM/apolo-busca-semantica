from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

def conectarMongo():

    uri = os.getenv("MONGO_URI")

    client = MongoClient(uri)

    db = client['Cluster0']

    return db