import dataclasses
from datetime import datetime
from flask import abort, Flask, jsonify, request

from sqlalchemy import create_engine, select, desc
from sqlalchemy import text  # TODO remove
from sqlalchemy.orm import sessionmaker

from asset_orm import Asset

app = Flask(__name__)

engine = create_engine("mysql://mysql/WealthDB")  # automatically handles connection pooling
Session = sessionmaker(engine)

@app.route('/assets', methods=['GET'])
def get_assets():

    with Session() as session:
        query = select(Asset)
        assets = session.scalars(query).all()

    return jsonify([dataclasses.asdict(asset) for asset in assets])

@app.route('/assets/<string:asset_id>', methods=['GET'])
def get_asset(asset_id):

    if request.args.get("asOf"):
        as_of = datetime.fromisoformat(request.args.get("asOf")) # TODO: date time format validation
    else:
        as_of = None

    with Session() as session:
        query = select(Asset).filter_by(assetId=asset_id).order_by(desc(Asset.balanceAsOf))

        if as_of:
            query = query.filter(Asset.balanceAsOf <= as_of)

        asset = session.scalars(query).first()

    if asset:
        return jsonify(dataclasses.asdict(asset))
    else:
        abort(404)

@app.route('/assets', methods=['POST'])
def create_asset():
    with Session() as session:
        try:
            # TODO: missing data validation of request body
            asset = Asset(**request.json)
            session.add(asset)
            session.commit()
            success = True
        except:
            session.rollback()
            success = False
        finally:
            session.close()

    return jsonify({"success": success})

