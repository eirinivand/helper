from helper.app import db

import sqlalchemy


def get_connection():
    return db.get_engine().connect()


def get_metadata():
    return sqlalchemy.MetaData()


def recreate_database():
    db.drop_all()
    db.create_all()
