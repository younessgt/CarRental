#!/usr/bin/python3
""" Creating the main Flask APP
for api """
from models import storage
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_session(exception):
    """ method to remove the current SQLAlchemy session """
    storage.close()


@app.errorhandler(404)
def error_handler(e):
    return {"error": "No Data found"}, 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5001)
    app.run(host=host, port=port, threaded=True)
