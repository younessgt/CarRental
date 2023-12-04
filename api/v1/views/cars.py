#!/usr/bin/python3
""" Handling the search car api """

from flask import abort, jsonify, request
from models import storage
from models.location import Location
from models.car import Car
from api.v1.views import app_views


@app_views.route('/car_search', methods=['POST'], strict_slashes=False)
def car_search():
    """ retreving all Car objects depending on the content of
    body request (JSON) """

    if request.get_json() is None:
        abort(404, description="Not a Json")

    data = request.get_json()

    """ checking if data exit or not and if empty or not """
    if data and len(data):
        location_id = data.get('location', None)
        price = data.get('price', None)

    if not data or not len(data) or (
            not location_id and
            not price):
        cars = storage.all(Car).values()
        car_list = []

        for car in cars:
            if car.rent_price == 120:
                car_list.append(car.to_dict())
        return jsonify(car_list)

    car_list = []

    """ retreving the location object from the request
      that come with locationId """

    if location_id:

        location_obj = [storage.get(Location, lo_id) for lo_id in location_id]
        for location in location_obj:
            for car in location.cars:
                car_list.append(car)

    """ if the user include the price to """
    if price and location_id:
        if int(price[0]) != 0:
            car_list = [car for car in car_list if car.rent_price == int(price[0])]

    if price and not location_id:
        cars = storage.all(Car).values()
        if int(price[0]) != 0:
            car_list = [car for car in cars if car.rent_price == int(price[0])]
        else:
            car_list = [car for car in cars]

    car_list_todict = []
    for car in car_list:
        car_list_todict.append(car.to_dict())
    return jsonify(car_list_todict)


@app_views.route('/cars', methods=['GET'], strict_slashes=False)
def cars():
    """ retrieving all cars """
    car_list = []
    cars = storage.all(Car).values()
    for car in cars:
        car_list.append(car.to_dict())
    return jsonify(car_list)


@app_views.route('/cars/<rent_price>', methods=['GET'], strict_slashes=False)
def car(rent_price):
    """ retreiving cars depending on the rent_price """
    try:
        price = int(rent_price)
    except ValueError:
        return jsonify({'error': '{} is not a number'.format(rent_price)})
    price_list = [70, 90, 120]

    if price in price_list:
        car_list = []
        cars = storage.all(Car).values()
        for car in cars:
            if car.rent_price == price:
                car_list.append(car.to_dict())
        return jsonify(car_list)
    else:
        return jsonify({'Sorry': 'No car was Found with this price'})


@app_views.route('/update_car_status/<car_id>/<new_status>', methods=['POST'], strict_slashes=False)
def update_car_status(car_id, new_status):
    """ updating the status of cars and returning True if success"""

    if storage.update_status(str(car_id), str(new_status)):
        return jsonify(success=True)
    return jsonify(success=False), 400
