from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .models import db, Note, Reminder
from .tasks import send_reminder_email

from datetime import datetime

bp = Blueprint('api/v1', __name__, url_prefix='/api/v1')

# Create Note
@bp.route('/notes', methods=['POST'])
def create_note():
  try:
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
      return jsonify({'error': 'Invalid input'}), 400
    
    new_note = Note(
      title=data['title'],
      content=data['content']
    )
    db.session.add(new_note)
    db.session.commit()
    return jsonify({
      'message': 'Note created.',
      'id': new_note.id
    }), 201
  
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'error': 'Database error', 'details': str(e)}), 500
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Read Note by Id
@bp.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
  try:
    note = Note.query.get_or_404(id)
    return jsonify({
      'id': note.id,
      'title': note.title,
      'content': note.content,
      'created_at': note.created_at,
      'updated_at': note.updated_at
    }), 200
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Read Notes
@bp.route('/notes', methods=['GET'])
def get_notes():
  try:
    notes = Note.query.all()
    return jsonify([{
      'id': note.id,
      'title': note.title,
      'content': note.content,
      'created_at': note.created_at,
      'updated_at': note.updated_at
    } for note in notes]), 200
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Update Note
@bp.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
  try:
    data = request.json
    if not data or 'title' not in data or 'content' not in data:
      return jsonify({'error': 'Invalid input'}), 400
    
    note = Note.query.get_or_404(id)
    note.title = data['title']
    note.content = data['content']
    db.session.commit()
    return jsonify({
      'id': note.id,
      'title': note.title,
      'content': note.content,
      'created_at': note.created_at,
      'updated_at': note.updated_at,}), 200
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'error': 'Database error', 'details': str(e)}), 500
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Delete Note
@bp.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
  try:
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note Deleted.'}), 200
  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'error': 'Database error', 'details': str(e)}), 500
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Schedule Reminder
@bp.route('/notes/<int:note_id>/reminder', methods=['POST'])
def schedule_reminder(note_id):
  try:
    data = request.json
    if not data or 'reminder_time' not in data or 'email' not in data:
      return jsonify({'error': 'Invalid input'}), 400

    _reminder_time = data['reminder_time']
    email = data['email']
    
    try:
      reminder_time = datetime.fromisoformat(_reminder_time)
    except ValueError:
      return jsonify({'error': 'Invalid datetime format'}), 400

    new_reminder = Reminder(
      note_id=note_id,
      reminder_time=reminder_time,
      email=email
    )
    db.session.add(new_reminder)
    db.session.commit()

    try:
      send_reminder_email.delay(new_reminder.id)
    except Exception as e:
      db.session.rollback()
      return jsonify({'error': 'Failed to schedule reminder', 'details': str(e)}), 500
    
    return jsonify({'message': 'Reminder Scheduled'}), 201

  except SQLAlchemyError as e:
    db.session.rollback()
    return jsonify({'error': 'Database error', 'details': str(e)}), 500
  except Exception as e:
    return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
