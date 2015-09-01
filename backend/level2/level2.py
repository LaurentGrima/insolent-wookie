from datetime import datetime
import json


class Rental(object):
    """ A class for rental management. """
    DECREASE = {
        1: 0.9,
        4: 0.7,
        10: 0.5,
    }

    def __init__(self, id, car_id, start_date, end_date, distance):
        self.id = id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance

    def get_rental_duration(self):
        """ Calculates the rental duration in days.

        Example: a rental starting and finishing the same date
            has a duration of 1 day.

        Returns:
            The duration as an Int.
        """
        d1 = datetime.strptime(self.start_date, "%Y-%m-%d")
        d2 = datetime.strptime(self.end_date, "%Y-%m-%d")
        return abs((d2 - d1).days) + 1

    def get_price(self, price_per_day, price_per_km):
        """ Calculates the rental total price.

        Args:
            price_per_day (Int)
            price_per_km (Int)

        Returns:
            The price as an Int.
        """
        # Note: Python does not have switches.
        duration = self.get_rental_duration()
        if duration > 10:
            return int(
                self.DECREASE[10] * (duration-10) * price_per_day +
                self.DECREASE[4] * 6 * price_per_day +
                self.DECREASE[1] * 3 * price_per_day +
                1 * price_per_day +
                self.distance * price_per_km
                )
        elif duration > 4:
            return int(
                self.DECREASE[4] * (duration-4) * price_per_day +
                self.DECREASE[1] * 3 * price_per_day +
                1 * price_per_day +
                self.distance * price_per_km
                )
        elif duration > 1:
            return int(
                self.DECREASE[1] * (duration-1) * price_per_day +
                1 * price_per_day +
                self.distance * price_per_km
                )
        else:
            return int(
                duration * price_per_day +
                self.distance * price_per_km
                )

with open('data.json') as json_data:
    input_data = json.load(json_data)
    # Using dict comprehension to create O(1) access to cars by id.
    cars = {car['id']: car for car in input_data['cars']}

    rentals = []
    for input_rental in input_data['rentals']:
        output_rental = Rental(
            input_rental['id'],
            input_rental['car_id'],
            input_rental['start_date'],
            input_rental['end_date'],
            input_rental['distance']
        )
        car = cars[output_rental.car_id]
        rentals.append({
            'id': output_rental.id,
            'price': output_rental.get_price(
                car['price_per_day'],
                car['price_per_km']
                )
            })

    # Output the json file.
    with open('_output.json', 'w') as outfile:
        json.dump({'rentals': rentals}, outfile)
