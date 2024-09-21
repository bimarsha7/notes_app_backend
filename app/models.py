from . import db
from datetime import datetime

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  created_at = db.Column(db.DateTime, default=db.func.now())
  updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

class Reminder(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  note_id = db.column(db.Integer, db.ForeignKey('note.id'))
  reminder_time = db.Column(db.DateTime, nullable=False)
  email = db.Column(db.String(120), nullable=False)
  is_sent = db.Column(db.Boolean, default=False)
