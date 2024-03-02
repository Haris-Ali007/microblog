import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-random-text'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'app.db')
    POST_PER_PAGE = 5
    