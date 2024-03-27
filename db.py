from pymongo import MongoClient
from dotenv import dotenv_values
config = dotenv_values(".env")

def get_db():
   client = MongoClient(f"mongodb+srv://admin:{config['MONGODB_PASSWORD']}@cluster0.pjslk37.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
   return client['varientportal']