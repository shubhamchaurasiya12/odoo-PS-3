from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import (
    get_pending_items, approve_item, reject_item, get_all_items,
    get_admin_users, make_user_admin, get_user_by_id
)

admin_bp = Blueprint('admin', __name__)

def require_admin(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in', 'error')
            return redirect(url_for('auth.login'))
        
        if not session.get('is_admin', False):
            flash('Admin access required', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/admin')
@require_admin
def admin_panel():
    pending_items = get_pending_items()
    all_items = get_all_items()
    return render_template('admin_panel.html', 
                         pending_items=pending_items, 
                         all_items=all_items)

@admin_bp.route('/admin/approve/<item_id>', methods=['POST'])
@require_admin
def approve_item_route(item_id):
    try:
        approve_item(item_id)
        flash('Item approved successfully', 'success')
    except Exception as e:
        flash('Error approving item', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/reject/<item_id>', methods=['POST'])
@require_admin
def reject_item_route(item_id):
    try:
        reject_item(item_id)
        flash('Item rejected successfully', 'success')
    except Exception as e:
        flash('Error rejecting item', 'error')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/make_admin/<user_id>', methods=['POST'])
@require_admin
def make_admin_route(user_id):
    try:
        make_user_admin(user_id)
        flash('User made admin successfully', 'success')
    except Exception as e:
        flash('Error making user admin', 'error')
    
    return redirect(url_for('admin.admin_panel')) 