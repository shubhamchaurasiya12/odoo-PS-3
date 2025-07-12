from flask import Flask, render_template, redirect, url_for, session, flash
from config import Config
from models.db import get_user_items, get_user_swaps, get_user_by_id
from auth.routes import auth_bp
from items.routes import items_bp
from admin.routes import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(admin_bp)


@app.route('/test-db')
def test_db():
    from models.db import db
    try:
        db.command("ping")  # MongoDB ping command
        return "MongoDB connection successful!"
    except Exception as e:
        return f"MongoDB connection failed: {str(e)}"
    
@app.route('/')
def home():
    """Landing page"""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        flash('Please log in to access dashboard', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    user_items = get_user_items(user_id)
    user_swaps = get_user_swaps(user_id)
    
    return render_template('dashboard.html', 
                         user_items=user_items, 
                         user_swaps=user_swaps)

@app.context_processor
def inject_user():
    """Inject user info into all templates"""
    user_info = None
    if 'user_id' in session:
        user_info = {
            'id': session['user_id'],
            'email': session['user_email'],
            'name': session['user_name'],
            'is_admin': session.get('is_admin', False)
        }
    return dict(user=user_info)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 