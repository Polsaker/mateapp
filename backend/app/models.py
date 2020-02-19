from playhouse.flask_utils import FlaskDB
from peewee import CharField, IntegerField, DateTimeField

from datetime import datetime

db_wrapper = FlaskDB()

class User(db_wrapper.Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    # Acá almacenamos con qué método está encriptada la pass.
    # 1 = bcrypt
    crypto = IntegerField(default=1)
    password = CharField(max_length=255)

    joindate = DateTimeField(default=datetime.utcnow)

    # Nombre (real?) del usuario
    name = CharField(null=True)
    # 0 si el usuario no está baneado
    status = IntegerField(default=0)