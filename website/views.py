# file storing routes for the website aka where the user can go
from flask import Blueprint, render_template, request, flash, jsonify
# this file will be a blueprint of the website - it has roots/URLs defined in it
# allows us to define routes in a separate file and then import them into the main file
from flask_login import login_required, current_user
from . import db
from .models import Note
import json

views = Blueprint('views', __name__)

# defining a route for in the views blueprint
@views.route('/', methods = ['GET', 'POST']) # / indicates the root of the website/homepage
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) == 0:
            flash("Note is empty!", category='error')
        else:
            flash("Note added!", category='success')
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})