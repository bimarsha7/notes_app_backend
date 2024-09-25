import os

class Config:
  def db_config_url():
    from sqlalchemy import create_engine
    from sqlalchemy.engine import URL

    # Connect to your postgres DB
    url = URL.create(
      drivername=os.getenv('DB_DRIVER', 'postgresql'),
      username=os.getenv('DB_USER', 'postgres'),
      password=os.getenv('DB_PASSWORD', 'postgres'),
      host=os.getenv('DB_HOST', 'localhost'),
      port=os.getenv('DB_PORT', '5432'),
      database=os.getenv('DB_NAME', 'notes_app'),
    )
    return create_engine(url).url
  print(db_config_url())
  SQLALCHEMY_DATABASE_URI = db_config_url()
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
  MAIL_PORT = os.getenv('MAIL_PORT', 587)
  MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
  MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'bmrsbhandari@gmail.com')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'iriekkhfhwdbfpaz')
  CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
  CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
