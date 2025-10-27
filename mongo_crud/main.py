from pymongo import MongoClient

client = MongoClient("mongodb+srv://goitlearn:20Ssibof%40@cluster0.tbiftdo.mongodb.net/?retryWrites=true&w=majority")


db = client["cats_db"]

cats_collection = db["cats"]

def add_cat(name, age, features):
    try:
        cat = {"name": name, "age": age, "features": features}
        cats_collection.insert_one(cat)
        print(f"✅ Cat {name} added!")
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
        print(f"No cat found with name {name}")

def add_feature(name, feature):
    result = cats_collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count:
        print(f"✅ Added feature '{feature}' for {name}")
    else:
        print(f"No cat found with name {name}")

def delete_cat(name):
    result = cats_collection.delete_one({"name": name})
    if result.deleted_count:
        print(f"✅ Deleted {name}")
    else:
        print(f"No cat found with name {name}")

def delete_all_cats():
    result = cats_collection.delete_many({})
    print(f"✅ Deleted {result.deleted_count} cats")

def main():
    while True:
        cmd = input("Choose action: list, find, add, update_age, add_feature, delete, delete_all, exit: ")
        if cmd == "list":
            list_cats()
        elif cmd == "find":
            find_cat(input("Name: "))
        elif cmd == "add":
            add_cat(input("Name: "), int(input("Age: ")), input("Features (comma separated): ").split(","))
        elif cmd == "update_age":
            update_age(input("Name: "), int(input("New Age: ")))
        elif cmd == "add_feature":
            add_feature(input("Name: "), input("Feature: "))
        elif cmd == "delete":
            delete_cat(input("Name: "))
        elif cmd == "delete_all":
            delete_all_cats()
        elif cmd == "exit":
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()

