import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, 'cantina-digitale')
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from app import app
import database

database.init_db()
database.init_abbinamenti_db()

if __name__ == '__main__':
    app.run()
