from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from config import Config
import os

# Initialize MongoDB connection
client = MongoClient(Config.MONGODB_URI)
db = client[Config.DATABASE_NAME]

# Collections
users_collection = db.users
items_collection = db.items
swaps_collection = db.swaps

def get_user_by_email(email):
    """Get user by email"""
    return users_collection.find_one({"email": email})

def get_user_by_id(user_id):
    """Get user by ID"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return users_collection.find_one({"_id": user_id})

def create_user(email, password_hash, name):
    """Create a new user"""
    user = {
        "email": email,
        "password": password_hash,
        "name": name,
        "is_admin": False,
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user

def get_all_items(status="Available", exclude_user_id=None):
    """Get all items with optional filtering"""
    query = {"status": status, "approved": True}
    if exclude_user_id:
        if isinstance(exclude_user_id, str):
            exclude_user_id = ObjectId(exclude_user_id)
        query["user_id"] = {"$ne": exclude_user_id}
    return list(items_collection.find(query).sort("created_at", -1))

def get_user_items(user_id):
    """Get all items uploaded by a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return list(items_collection.find({"user_id": user_id}).sort("created_at", -1))

def get_item_by_id(item_id):
    """Get item by ID"""
    if isinstance(item_id, str):
        item_id = ObjectId(item_id)
    return items_collection.find_one({"_id": item_id})

def create_item(user_id, title, description, category, item_type, size, condition, tags, image_url):
    """Create a new item"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    item = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "category": category,
        "type": item_type,
        "size": size,
        "condition": condition,
        "tags": tags,
        "image_url": image_url,
        "status": "Available",
        "approved": False,  # Admin approval required
        "created_at": datetime.utcnow()
    }
    result = items_collection.insert_one(item)
    item["_id"] = result.inserted_id
    return item

def get_pending_items():
    """Get all items pending admin approval"""
    return list(items_collection.find({"approved": False}).sort("created_at", -1))

def approve_item(item_id):
    """Approve an item"""
    if isinstance(item_id, str):
        item_id = ObjectId(item_id)
    return items_collection.update_one(
        {"_id": item_id},
        {"$set": {"approved": True}}
    )

def reject_item(item_id):
    """Reject/delete an item"""
    if isinstance(item_id, str):
        item_id = ObjectId(item_id)
    return items_collection.delete_one({"_id": item_id})

def create_swap_request(item1_id, item2_id, requested_by):
    """Create a new swap request"""
    if isinstance(item1_id, str):
        item1_id = ObjectId(item1_id)
    if isinstance(item2_id, str):
        item2_id = ObjectId(item2_id)
    if isinstance(requested_by, str):
        requested_by = ObjectId(requested_by)
    
    swap = {
        "item1_id": item1_id,
        "item2_id": item2_id,
        "status": "Pending",
        "requested_by": requested_by,
        "created_at": datetime.utcnow()
    }
    result = swaps_collection.insert_one(swap)
    swap["_id"] = result.inserted_id
    return swap

def get_user_swaps(user_id):
    """Get all swaps involving a user"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    
    # Get items owned by user
    user_items = list(items_collection.find({"user_id": user_id}, {"_id": 1}))
    user_item_ids = [item["_id"] for item in user_items]
    
    # Find swaps where user's items are involved
    swaps = list(swaps_collection.find({
        "$or": [
            {"item1_id": {"$in": user_item_ids}},
            {"item2_id": {"$in": user_item_ids}},
            {"requested_by": user_id}
        ]
    }).sort("created_at", -1))
    
    return swaps

def get_admin_users():
    """Get all admin users"""
    return list(users_collection.find({"is_admin": True}))

def make_user_admin(user_id):
    """Make a user an admin"""
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)
    return users_collection.update_one(
        {"_id": user_id},
        {"$set": {"is_admin": True}}
    ) 