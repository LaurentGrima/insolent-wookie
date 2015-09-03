from datetime import datetime


class Rental(object):
    """ A class for rental management.

    Attributes:
        id (int)
        car (Car): a Car instance.
        start_date (date): Rental start date.
        end_date (date): Rental end date.
        distance (int): distance diven (km) expected for th rental period.
        deductible_reduction (boolean): Option for the driver to reduce
            the deductible amount from €800 to €150,
            for a few more euros per day.
        DECREASE (list[Dict]): Holds rates for price per day discounts
            and duration threshold.
            The threshold is the minimum duration at which the rate applies.
            The final rate is 'decrease rate' * 'origin cost per day'.
        COMMISSION_RATE (float): The rate used to calculate the commission.

    """
    DECREASE = [
        {'rate': 0.5, 'threshold': 10},
        {'rate': 0.7, 'threshold': 4},
        {'rate': 0.9, 'threshold': 1},
        ]
    COMMISSION_RATE = 0.3
    DEDUCTIBLE_DAILY_FEE = 400

    def __init__(self, id, car, start_date, end_date,
                 distance, deductible_reduction):
        self.id = id
        self.car = car
        self.start_date = start_date
        self.end_date = end_date
        self.distance = distance
        self.deductible_reduction = deductible_reduction

    def get_duration(self):
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

        Rules apply as follows:
        New rules:
            - price per day decreases by 0.10 after 1 day
            - price per day decreases by 0.30 after 4 days
            - price per day decreases by 0.50 after 10 days

        Returns:
            The price as an Int.
        """
        duration = self.get_duration()
        diff1 = max(duration - self.DECREASE[0]['threshold'], 0)
        diff2 = max(duration - diff1 - self.DECREASE[1]['threshold'], 0)
        diff3 = max(duration - diff1 - diff2 - self.DECREASE[2]['threshold'], 0)
        total_price_per_day = (
            self.DECREASE[0]['rate'] * diff1 +
            self.DECREASE[1]['rate'] * diff2 +
            self.DECREASE[2]['rate'] * diff3 +
            1) * self.car.price_per_day

        total_price_per_km = self.distance * self.car.price_per_km

        return round(total_price_per_day + total_price_per_km)

    def get_commission(self):
        """ Calculates the commission.

        Returns:
            A dictionary containing the differents fees.
        """
        price = self.get_price()
        commission_total = price * self.COMMISSION_RATE
        insurance_fee = round(commission_total / 2)
        assistance_fee = round(self.get_duration() * 100)
        drivy_fee = round(max(
            commission_total - (insurance_fee + assistance_fee),
            0))
        return {
            'insurance_fee': insurance_fee,
            'assistance_fee': assistance_fee,
            'drivy_fee': drivy_fee
        }

    def get_deductible_reduction(self):
        """ Calculates the deductible reduction cost if applicable.

        Returns:
            The cost as an Int (0 if the deductible_reduction reduction
                was not chosen).
        """
        if self.deductible_reduction:
            return self.get_duration() * self.DEDUCTIBLE_DAILY_FEE
        else:
            return 0

    def options(self):
        return {'deductible_reduction': self.get_deductible_reduction()}

    def get_actions(self):
        """ Shows how much money must be debited/credited for each actor. """
        commission = self.get_commission()
        deductible_reduction = self.get_deductible_reduction()
        return [
            {
              "who": "driver",
              "type": "debit",
              "amount": self.get_price() + deductible_reduction
            },
            {
              "who": "owner",
              "type": "credit",
              "amount": self.get_price() - sum(commission.values())
            },
            {
              "who": "insurance",
              "type": "credit",
              "amount": commission['insurance_fee']
            },
            {
              "who": "assistance",
              "type": "credit",
              "amount": commission['assistance_fee']
            },
            {
              "who": "drivy",
              "type": "credit",
              "amount": commission['drivy_fee'] + deductible_reduction
            }
        ]
