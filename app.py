import dataclasses
from datetime import datetime
import json

from flask import abort, Flask, jsonify, request
from flask.json.provider import JSONProvider
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker

from asset_orm import Asset

class CustomJSONEncoder(json.JSONEncoder):
    """Flask's jsonify is formatting datetimes as "Fri, 28 Mar 2025 15:55:22 GMT". Use this custom json encoder
    to force ISO 8601 format"""
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)

class CustomJSONProvider(JSONProvider):

    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder, indent=2)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)

app = Flask(__name__)
app.json = CustomJSONProvider(app)

engine = create_engine("mysql://mysql/WealthDB")  # automatically handles connection pooling
Session = sessionmaker(engine)

@app.route('/assets', methods=['GET'])
def get_assets():
    """Returns all assets in the database.

    Future work:
    - only return the latest version of each asset id
    - implement pagination to reduce amount of data returned
    """

    with Session() as session:
        query = select(Asset)
        assets = session.scalars(query).all()

    return jsonify([dataclasses.asdict(asset) for asset in assets])

@app.route('/assets/<string:asset_id>', methods=['GET'])
def get_asset(asset_id):
    """Returns the asset data for a specific asset_id.
    
    If an asOf query parameter is passed with a date, this will return
    the latest version of the asset entry on or before that date.
    """

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
        app.logger.info(dataclasses.asdict(asset))
        app.logger.info(jsonify(dataclasses.asdict(asset)))
        return jsonify(dataclasses.asdict(asset))
    else:
        abort(404)

@app.route('/assets', methods=['POST'])
def create_asset():
    """Creates a new asset entry.

    Assumes that request was sent with "Content-Type: application/json" header
    """

    with Session() as session:
        try:
            # TODO: missing data validation of request body
            asset = Asset(**request.json)
            session.add(asset)
            session.commit()
            success = True
        except Exception as e:
            session.rollback()
            app.logger.error(e)
            success = False
        finally:
            session.close()

    return jsonify({"success": success})

