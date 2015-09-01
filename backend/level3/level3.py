from datetime import datetime
import json


class Rental(object):
    """ A class for rental management. """
    DECREASE = {
        1: 0.9,
        4: 0.7,
        10: 0.5,
    }
    COMMISSION_RATE = 0.3

    def __init__(self, id, car, start_date, end_date, distance):
        self.id = id
        self.car = car
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

    def get_price(self):
        """ Calculates the rental total price.

        Returns:
            The price as an Int.
        """
        # Note: Python does not have switches.
        duration = self.get_rental_duration()
        if duration > 10:
            return int(
                self.DECREASE[10] * (duration-10) * self.car['price_per_day'] +
                self.DECREASE[4] * 6 * self.car['price_per_day'] +
                self.DECREASE[1] * 3 * self.car['price_per_day'] +
                1 * self.car['price_per_day'] +
                self.distance * self.car['price_per_km']
                )
        elif duration > 4:
            return int(
                self.DECREASE[4] * (duration-4) * self.car['price_per_day'] +
                self.DECREASE[1] * 3 * self.car['price_per_day'] +
                1 * self.car['price_per_day'] +
                self.distance * self.car['price_per_km']
                )
        elif duration > 1:
            return int(
                self.DECREASE[1] * (duration-1) * self.car['price_per_day'] +
                1 * self.car['price_per_day'] +
                self.distance * self.car['price_per_km']
                )
        else:
            return int(
                duration * self.car['price_per_day'] +
                self.distance * self.car['price_per_km']
                )

    def get_commission(self):
        """ Calculates the commission.

        Returns:
            A dictionary containing the differents fees.
        """
        price = self.get_price()
        commission_total = price * self.COMMISSION_RATE
        insurance_fee = int(commission_total * 0.5)
        assistance_fee = int(self.get_rental_duration() * 100)
        drivy_fee = int(max(
            commission_total - (insurance_fee + assistance_fee),
            0))
        return {
            'insurance_fee': insurance_fee,
            'assistance_fee': assistance_fee,
            'drivy_fee': drivy_fee
        }


with open('data.json') as json_data:
    input_data = json.load(json_data)
    # Using dict comprehension to create O(1) access to cars by id.
    cars = {car['id']: car for car in input_data['cars']}

    rentals = []
    for input_rental in input_data['rentals']:
        output_rental = Rental(
            input_rental['id'],
            cars[input_rental['car_id']],
            input_rental['start_date'],
            input_rental['end_date'],
            input_rental['distance']
        )
        rentals.append({
            'id': output_rental.id,
            'price': output_rental.get_price(),
            'commission': output_rental.get_commission()
            })

    # Output the json file.
    with open('_output.json', 'w') as outfile:
        json.dump({'rentals': rentals}, outfile)
