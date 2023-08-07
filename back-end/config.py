import os
from dotenv import load_dotenv, dotenv_values

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), encoding='utf-8')
env = dotenv_values(os.path.join(basedir, '.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///onlinetesting.db'
    SECRET_KEY = env['SECRET_KEY']
