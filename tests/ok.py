import pymongo
from pymongo import MongoClient
import random
from faker import Faker

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['pharma']
collection = db['pharmacies']

# List of medicines
medicines = [
    "Dolo", "Vicks", "Aspirin", "Paracetamol", "Ibuprofen", "Amoxicillin", "Ciprofloxacin",
    "Omeprazole", "Metformin", "Simvastatin", "Lisinopril", "Levothyroxine",
    "Atorvastatin", "Azithromycin", "Prednisone", "Albuterol", "Doxycycline",
    "Fluoxetine", "Losartan", "Warfarin", "Ranitidine", "Pantoprazole"
]
def fake_phone_number(fake: Faker) -> str:
    return f'+91 {fake.msisdn()[3:]}'

# Function to generate random pharmacy data
def generate_pharmacy():
    fake = Faker()
    pharmacy = {
        "name": fake.company() + " Pharmacy",
        "items": [],
        "owner": fake.name().lower(),
        "lat": random.uniform(29, 31),
        "long": random.uniform(75, 77),
        "phone": fake_phone_number(fake),
        "rating": random.randint(3, 5)  # Adding random rating between 1 and 5
    }
    # Adding random medicines to the pharmacy
    chosen_medicines = set()
    for _ in range(random.randint(1, 20)):
        while True:
            medicine_name = random.choice(medicines)
            if medicine_name not in chosen_medicines:
                break
        chosen_medicines.add(medicine_name)
        medicine = {
            "name": medicine_name.lower(),
            "quantity": random.randint(1, 1000),
            "price": random.randint(1, 100)
        }
        pharmacy["items"].append(medicine)
    return pharmacy

# Inserting records into the collection
for _ in range(22):
    pharmacy_data = generate_pharmacy()
    collection.insert_one(pharmacy_data)

print("Records inserted successfully.")
