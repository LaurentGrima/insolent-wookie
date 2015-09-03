import json

from models.car import Car
from models.rentalmodification import RentalModification
from models.rental import Rental


with open('data.json') as json_data:
    input_data = json.load(json_data)
    # Using dict comprehension to create O(1) access to cars by id.
    cars = {
        car['id']: Car(car['id'], car['price_per_day'], car['price_per_km'])
        for car in input_data['cars']
        }

    rentals = {}
    for input_rental in input_data['rentals']:
        output_rental = Rental(
            input_rental['id'],
            cars[input_rental['car_id']],
            input_rental['start_date'],
            input_rental['end_date'],
            input_rental['distance'],
            input_rental['deductible_reduction'],
        )
        rentals[output_rental.id] = output_rental

    rental_modifications = []
    for input_modification in input_data['rental_modifications']:
        output_modification = RentalModification(
            input_modification['id'],
            rentals[input_modification['rental_id']],
            input_modification.get('start_date', None),
            input_modification.get('end_date', None),
            input_modification.get('distance', None)
            )
        rental_modifications.append(output_modification.compute_delta())

    # Output the json file.
    with open('_output.json', 'w') as outfile:
        json.dump({'rental_modifications': rental_modifications}, outfile)
