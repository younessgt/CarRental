#!/usr/bin/python3
""" Flask Web app """

from models import storage
from models.location import Location
from models.car import Car
from flask import Flask, render_template
import uuid
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/', strict_slashes=False)
def home():
    """ home page """
    locations = storage.all(Location).values()
    locations = sorted(locations, key=lambda k: k.name)
    cars = storage.all(Car).values()
    cars = sorted(cars, key=lambda k: k.name)
    cache_id = str(uuid.uuid4())

    return render_template('index.html', locations=locations,
                           cars=cars, cache_id=cache_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
