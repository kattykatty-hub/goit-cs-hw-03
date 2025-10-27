import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI securely
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("❌ MongoDB URI not found. Please create a .env file with MONGO_URI variable.")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["cats_db"]
    cats_collection = db["cats"]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    exit(1)

# === CRUD FUNCTIONS ===

def add_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        cats_collection.insert_one(cat)
        print(f"✅ Cat '{name}' added!")
    except Exception as e:
        print(f"❌ Error adding cat: {e}")

def list_cats():
    for cat in cats_collection.find():
        print(cat)

def find_cat(name):
    cat = cats_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"❌ No cat found with name '{name}'")

def update_age(name, new_age):
    result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count:
        print(f"✅ Updated {name}'s age to {new_age}")
    else:
        print(f"❌ No cat found with name '{name}'")

def add_feature(name, feature):
    result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count:
        print(f"✅ Added feature '{feature}' for {name}")
    else:
        print(f"❌ No cat found with name '{name}'")

def delete_cat(name):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"✅ Deleted '{name}'")
    else:
        print(f"❌ No cat found with name '{name}'")

def delete_all_cats():
    result = cats_collection.delete_many({})
    print(f"✅ Deleted {result.deleted_count} cats")

# === MAIN MENU ===

def main():
    while True:
        cmd = input(
            "\nChoose action: list, find, add, update_age, add_feature, delete, delete_all, exit: "
        ).strip().lower()

        if cmd == "list":
            list_cats()
        elif cmd == "find":
            find_cat(input("Name: ").strip())
        elif cmd == "add":
            name = input("Name: ").strip()
            age = int(input("Age: "))
            features = input("Features (comma separated): ").split(",")
            features = [f.strip() for f in features if f.strip()]
            add_cat(name, age, features)
        elif cmd == "update_age":
            update_age(input("Name: ").strip(), int(input("New Age: ")))
        elif cmd == "add_feature":
            add_feature(input("Name: ").strip(), input("Feature: ").strip())
        elif cmd == "delete":
            delete_cat(input("Name: ").strip())
        elif cmd == "delete_all":
            delete_all_cats()
        elif cmd == "exit":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Unknown command")

if __name__ == "__main__":
    main()
