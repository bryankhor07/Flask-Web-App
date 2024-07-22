from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, Image
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') # Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Providing the schema for the note 
            db.session.add(new_note) # Adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # This function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) # Returns an empty JSON object

@views.route('/delete-image', methods=['POST'])
def delete_image():
    data = request.get_json()
    imageId = data.get('imageId')
    image = Image.query.get(imageId)
    if image:
        if image.user_id == current_user.id:
            db.session.delete(image)
            db.session.commit()
            return jsonify({"message": "Image deleted"}), 200
    return jsonify({"error": "Unauthorized or image not found"}), 403

@views.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    data = request.get_json()
    userId = data.get('userId')
    user = User.query.get(userId)
    if user and user.id == current_user.id:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"error": "Unauthorized or user not found"}), 403