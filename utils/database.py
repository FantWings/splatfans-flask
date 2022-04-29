from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# 实例化SQL Alchemy
db: sqlalchemy = SQLAlchemy()
session = db.session
