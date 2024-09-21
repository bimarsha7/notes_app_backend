import os

class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///notes.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
  MAIL_PORT = os.getenv('MAIL_PORT', 587)
  MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
  MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bmrsbhandari@gmail.com')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'iriekkhfhwdbfpaz')
  CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
  CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
