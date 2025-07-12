from werkzeug.security import generate_password_hash, check_password_hash
import re

def hash_password(password):
    """Hash a password using werkzeug"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Check if a password matches its hash"""
    return check_password_hash(password_hash, password)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid" 