import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from asset_orm import Base, Asset

with open("assets.json", "r") as assets_json:
    assets = json.load(assets_json)

engine = create_engine("mysql://mysql/WealthDB")
Session = sessionmaker(engine)

# create database
if not database_exists(engine.url):
    print("Creating database ... ")
    create_database(engine.url)

# create tables from ORM
print("Creating table ... ")
Base.metadata.create_all(engine)

# insert data into table
with Session() as session:
    print("Inserting data ... ")
    try:
        for asset in assets:
            asset_obj = Asset(**asset)
            session.add(asset_obj)
        session.commit()
        # TODO output some stats about what it did
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
