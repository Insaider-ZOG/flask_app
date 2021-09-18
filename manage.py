import os

from flask_web.models import dbase
from flask_web import create_app
from flask_web.config import DB_NAME


if __name__ == ('__main__'):
    if not os.path.exists(DB_NAME):
        dbase.create_all(app=create_app())
    manager = create_app()
    manager.run()



# set FLASK_APP=manage.py