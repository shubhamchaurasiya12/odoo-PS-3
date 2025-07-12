from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from models.db import (
    get_all_items, get_user_items, get_item_by_id, create_item, 
    create_swap_request, get_user_swaps, get_user_by_id
)
from werkzeug.utils import secure_filename
import os
from datetime import datetime

items_bp = Blueprint('items', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    """Save uploaded image and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to make filename unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        
        # Ensure upload directory exists
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f"uploads/{filename}"
    return None

@items_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        flash('Please log in to upload items', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        item_type = request.form.get('type')
        size = request.form.get('size')
        condition = request.form.get('condition')
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # Validation
        if not all([title, description, category, item_type, size, condition]):
            flash('All fields are required', 'error')
            return render_template('upload.html')
        
        # Handle image upload
        image_file = request.files.get('image')
        if not image_file:
            flash('Image is required', 'error')
            return render_template('upload.html')
        
        image_url = save_image(image_file)
        if not image_url:
            flash('Invalid image format. Please use PNG, JPG, JPEG, or GIF', 'error')
            return render_template('upload.html')
        
        # Create item
        try:
            item = create_item(
                session['user_id'], title, description, category, 
                item_type, size, condition, tags, image_url
            )
            flash('Item uploaded successfully! It will be reviewed by admin.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Error uploading item. Please try again.', 'error')
            return render_template('upload.html')
    
    return render_template('upload.html')

@items_bp.route('/items')
def browse_items():
    user_id = session.get('user_id')
    items = get_all_items(exclude_user_id=user_id)
    return render_template('items.html', items=items)

@items_bp.route('/item/<item_id>')
def item_detail(item_id):
    item = get_item_by_id(item_id)
    if not item:
        flash('Item not found', 'error')
        return redirect(url_for('items.browse_items'))
    
    # Get uploader info
    uploader = get_user_by_id(item['user_id'])
    
    return render_template('item_detail.html', item=item, uploader=uploader)

@items_bp.route('/item/<item_id>/request_swap', methods=['POST'])
def request_swap(item_id):
    if 'user_id' not in session:
        flash('Please log in to request swaps', 'error')
        return redirect(url_for('auth.login'))
    
    # Get the item being requested
    requested_item = get_item_by_id(item_id)
    if not requested_item:
        flash('Item not found', 'error')
        return redirect(url_for('items.browse_items'))
    
    # Get user's item for swap
    user_item_id = request.form.get('user_item_id')
    if not user_item_id:
        flash('Please select an item to swap', 'error')
        return redirect(url_for('items.item_detail', item_id=item_id))
    
    user_item = get_item_by_id(user_item_id)
    if not user_item or str(user_item['user_id']) != session['user_id']:
        flash('Invalid item selected', 'error')
        return redirect(url_for('items.item_detail', item_id=item_id))
    
    # Create swap request
    try:
        swap = create_swap_request(user_item_id, item_id, session['user_id'])
        flash('Swap request sent successfully!', 'success')
    except Exception as e:
        flash('Error creating swap request. Please try again.', 'error')
    
    return redirect(url_for('items.item_detail', item_id=item_id)) 