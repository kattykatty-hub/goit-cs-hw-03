import os
from pymongo import MongoClient
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError(" MongoDB URI not found. Please create a .env file with MONGO_URI variable.")

# === Connect to MongoDB ===
try:
    client = MongoClient(MONGO_URI)
    db = client["cats_db"]
    cats_collection = db["cats"]
    print(" Connected to MongoDB successfully!")
except Exception as e:
    print(f" Failed to connect to MongoDB: {e}")
    exit(1)

# === CRUD FUNCTIONS ===

def add_cat(name, age, features):
    """Create a new cat document."""
    try:
        cat = {"name": name, "age": age, "features": features}
        result = cats_collection.insert_one(cat)
        if result.inserted_id:
            print(f" Cat '{name}' added successfully!")
        else:
            print(" Cat was not added (unknown reason).")
    except Exception as e:
        print(f" Error adding cat: {e}")

def list_cats():
    """List all cats."""
    try:
        cats = list(cats_collection.find())
        if cats:
            for cat in cats:
                print(cat)
        else:
            print(" No cats found.")
    except Exception as e:
        print(f" Error reading cats: {e}")

def find_cat(name):
    """Find a cat by name."""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f" No cat found with name '{name}'.")
    except Exception as e:
        print(f" Error finding cat: {e}")

def update_age(name, new_age):
    """Update cat age by name."""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            if result.modified_count:
                print(f" Updated {name}'s age to {new_age}.")
            else:
                print(f" {name}'s age was already {new_age}. No changes made.")
        else:
            print(f" No cat found with name '{name}'.")
    except Exception as e:
        print(f" Error updating age: {e}")

def add_feature(name, feature):
    """Add new feature to a cat."""
    try:
        result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count:
            if result.modified_count:
                print(f" Added feature '{feature}' for {name}.")
            else:
                print(f" Feature '{feature}' already exists for {name}.")
        else:
            print(f" No cat found with name '{name}'.")
    except Exception as e:
        print(f" Error adding feature: {e}")

def delete_cat(name):
    """Delete a cat by name."""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"🗑️ Deleted '{name}'.")
        else:
            print(f" No cat found with name '{name}'.")
    except Exception as e:
        print(f" Error deleting cat: {e}")

def delete_all_cats():
    """Delete all cats."""
    try:
        result = cats_collection.delete_many({})
        print(f"🧹 Deleted {result.deleted_count} cats.")
    except Exception as e:
        print(f" Error deleting all cats: {e}")

# === MAIN MENU ===

def main():
    while True:
        cmd = input(
            "\nChoose action: list, find, add, update_age, add_feature, delete, delete_all, exit: "
        ).strip().lower()

        try:
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
                print(" Goodbye!")
                break
            else:
                print(" Unknown command")
        except Exception as e:
            print(f" Unexpected error: {e}")

if __name__ == "__main__":
    main()
