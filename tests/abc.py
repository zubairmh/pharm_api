from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["pharma"]
collection = db["pharmacies"]


# Define the list of medicines and their quantities needed
medicines_needed = [
    {"name": "dolo", "quantity": 10},
    {"name": "paracetamol", "quantity": 10},
    # Add more medicines if needed
]

# Construct query to match all medicines with their respective quantities
query = {
    "items": {
        "$all": [
            {"$elemMatch": {"name": m["name"], "quantity": {"$gte": m["quantity"]}}}
            for m in medicines_needed
        ]
    }
}

# Query the collection
results = collection.find(query)

# Print the pharmacies where all requirements are met
for result in results:
    print("Pharmacy:", result["name"])
    print("Items:", result["items"])


query = {"name": "Gupta Pharmacy"}
update = {"$inc": {"items.$[elem].quantity": -m["quantity"] for m in medicines_needed}}
out = collection.update_one(
    query,
    update,
    array_filters=[{"elem.name": {"$in": [m["name"] for m in medicines_needed]}}],
)
print(out)

# pharmacy_doc = {
#     "name": "Gupta Pharmacy",
#     "items": [
#         {"name": "dolo", "quantity": 30},
#         {"name": "paracetamol", "quantity": 60}
#     ]
# }

# # Insert the document into the collection
# result = collection.insert_one(pharmacy_doc)

# # Print the inserted document's ID
# print("Inserted document ID:", result.inserted_id)
