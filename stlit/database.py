from pymongo import MongoClient
from dotenv import load_dotenv
import os 

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["recipe_db"]
collection = db["user_preferences"]


# CRUD 

# CREATE
def add_user(user_id): 
    """Add a new user to the database."""
    user_data = { 
        "_id": user_id, 
        "preferences": [], 
        "recipe_history": []
    }
    try: 
        collection.insert_one(user_data)
        print(f"User {user_id} added successfully.")
    except Exception as e: 
        print(f"Error adding user: {e}")



# READ
def get_user(user_id): 
    """Retrieve username by user_id"""
    try: 
        user = collection.find_one({"_id":user_id})
    except Exception as e: 
        print(f"Error retrieving user: {e}")
        return None


def get_user_preferences(user_id): 
    """Get user preferences"""
    try: 
        prefs = collection.find_one({"_id":user_id})
    except Exception as e: 
        print(f"Error getting preferences: {e}") 
        return None
    
def get_user_history(user_id): 
    """Get user history"""
    try: 
        user = collection.find_one({"_id": user_id})
    except Exception as e: 
        print(f"Error getting user history: {e}")
        return None

# UPDATE
def add_to_recipe_history(user_id, recipe_id): 
    """Update recipe history"""
    try: 
        collection.update_one(
            {"_id":user_id}, 
            {"$push":{"recipe_history":recipe_id}}
        )
    except Exception as e: 
        print(f"Error adding to recipe history: {e}")

def update_user_preferences(user_id, preferences): 
    """Update a user's preferences."""
    try: 
        collection.update_one(
            {"_id": user_id}, 
            {"$set": {"preferences": preferences}}
        )
    except Exception as e: 
        print(f"Error updating user preferences: {e}")

# DELETE
def remove_user(user_id): 
    """Remove user from database"""
    result = collection.delete_one({"user_id": user_id})
    return result.deleted_count>0
