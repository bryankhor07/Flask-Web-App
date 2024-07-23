import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Image, Task
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

UPLOAD_FOLDER = 'website/static/profile_pics'
GALLERY_FOLDER = 'website/static/gallery_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        file = request.files['profilePicture']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            profile_picture_path = f'static/profile_pics/{filename}'
        else:
            profile_picture_path = None

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(first_name) < 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif len(last_name) < 2:
            flash("Last name must be greater than 2 characters.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1), profile_picture=profile_picture_path)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created.", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/profile-page')
def profile_page():
    return render_template("profile_page.html", user=current_user)

@auth.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        image = request.files['image']
        name = request.form.get('name')
        description = request.form.get('description')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(GALLERY_FOLDER, filename))
            image_path = f'static/gallery_images/{filename}'
        else:
            image_path = None

        new_image = Image(image=image_path, name=name, description=description, user_id=current_user.id)
        db.session.add(new_image)
        db.session.commit()
        flash("Image uploaded.", category='success')
        return redirect(url_for('auth.gallery'))
    return render_template("gallery.html", user=current_user)

@auth.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task = request.form.get('task')
        category = request.form.get('category')

        if len(task) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Task(data=task, category=category, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added!', category='success')
    return render_template("tasks.html", user=current_user)

@auth.route('/weather-page')
def weather():
    return render_template("weather.html", user=current_user)