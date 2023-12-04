#!/usr/bin/python3

from models.location import Location
from models.car import Car
from models import storage


""" locations """
claremont = Location(name="Claremont")
glendora = Location(name="Glendora")
malibu = Location(name="Malibu")

""" cars """

""" 75 $ """
car2 = Car(name="Passat CC", fuel="Gasoline", rent_price=75, status="unbooked")
car3 = Car(name="Mercedes C220", fuel="Gasoline", rent_price=75, status="unbooked")
car4 = Car(name="Golf Polo", fuel="Diesel", rent_price=75, status="unbooked")
car5 = Car(name="Mercedes C200", fuel="Gasoline", rent_price=75, status="unbooked")
car6 = Car(name="Bmw X1", fuel="Gasoline", rent_price=75, status="unbooked")
car7 = Car(name="Toyota Tundra", fuel="Diesel", rent_price=75, status="unbooked")

""" 120 $ """
car8 = Car(name="Mercedes GLE", fuel="Gasoline", rent_price=120, status="unbooked")
car9 = Car(name="Bmw X6", fuel="Diesel", rent_price=120, status="unbooked")
car10 = Car(name="Volkswagen Beetle", fuel="Gasoline", rent_price=120, status="unbooked")
car11 = Car(name="Mercedes ClassE", fuel="Diesel", rent_price=120, status="unbooked")
car12 = Car(name="Jaguar XF", fuel="Gasoline", rent_price=120, status="unbooked")

""" 350 $ """
car13 = Car(name="Bmw I8", fuel="Gasoline", rent_price=350, status="unbooked")
car14 = Car(name="Audi TT", fuel="Gasoline", rent_price=350, status="unbooked")
car15 = Car(name="Mercedes Cabriolet", fuel="Gasoline", rent_price=350, status="unbooked")
car16 = Car(name="Porsche 911", fuel="Gasoline", rent_price=350, status="unbooked")
car17 = Car(name="Bmw M3", fuel="Gasoline", rent_price=350, status="unbooked")

list_obj = [claremont, glendora, malibu, car2, car3,
            car4, car5, car6, car7, car8, car9, car10, car11, car12,
            car13, car14, car15, car16, car17]
storage.add(list_obj)
storage.save()

""" appending cars object to cars Location attribute and then
we can see that the car_location now have the data"""

claremont.cars.extend([car2, car3, car5, car6, car7])
glendora.cars.extend([car2, car3, car4, car6])
malibu.cars.extend([car5, car3, car4, car7])


claremont.cars.extend([car8, car9, car10])
glendora.cars.extend([car8, car10, car9, car12])
malibu.cars.extend([car8, car11, car12])


claremont.cars.extend([car16, car14, car13])
glendora.cars.extend([car17, car15, car13])
malibu.cars.extend([car13, car14, car15, car16, car17])

storage.save()

print("------ all cars in Malibu location -------")
for car in malibu.cars:
    print(car.name)

print("------ all locations where Bmw Serie 3 exist")
for location in car4.location:
    print(location.name)

print("--------- all method ------")
list_obj = storage.all(Location)

for obj in list_obj.values():
    print(obj.name)
print("------- get method -----")
obj1 = storage.get(Car, car4.id)
print(obj1.name)
