from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import get_user_by_email, create_user
from auth.utils import hash_password, check_password, validate_email, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        name = request.form.get('name')
        
        # Validation
        if not email or not password or not confirm_password or not name:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return render_template('register.html')
        
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('register.html')
        
        # Check if user already exists
        existing_user = get_user_by_email(email)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create user
        password_hash = hash_password(password)
        user = create_user(email, password_hash, name)
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))  # NOTE: 'auth.login' refers to the Blueprint and route name
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('login.html')
        
        user = get_user_by_email(email)
        if not user or not check_password(user['password'], password):
            flash('Invalid email or password', 'error')
            return render_template('login.html')
        
        # Store user info in session
        session['user_id'] = str(user['_id'])
        session['user_email'] = user['email']
        session['user_name'] = user['name']
        session['is_admin'] = user.get('is_admin', False)
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home')) 