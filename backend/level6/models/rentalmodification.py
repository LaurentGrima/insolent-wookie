import copy

from models.rental import Rental


class RentalModification(object):
    """ A class managing rental modifications.
    Attributes:
        id (int)
        rental (Rental): the rental being modified.
        start_date (date, optional): Rental modified start date.
        end_date (date, optional): Rental modified end date.
        distance (int, optional): Rental modified distance.
    """
    def __init__(self, id, rental, start_date=None, end_date=None,
                 distance=None):
        self.id = id
        self.rental = rental
        self.start_date = start_date if start_date else rental.start_date
        self.end_date = end_date if end_date else rental.end_date
        self.distance = distance if distance else rental.distance

    def compute_delta(self):
        """ Computes cost deltas from rental modifications. """
        modified_rental = copy.deepcopy(self.rental)
        modified_rental.start_date = self.start_date
        modified_rental.end_date = self.end_date
        modified_rental.distance = self.distance
        # Compute delta between the two actions lists.
        actions = zip(modified_rental.get_actions(), self.rental.get_actions())
        # toggle_dict[<a type>] returns the other type
        toggle_dict = {'debit': 'credit', 'credit': 'debit'}
        action_deltas = []
        for pair_of_actions in actions:
            delta = pair_of_actions[0]['amount'] - pair_of_actions[1]['amount']
            action_type = pair_of_actions[0]['type']
            who = pair_of_actions[0]['who']
            if delta < 0:
                delta = abs(delta)
                action_type = toggle_dict[action_type]
            action_deltas.append({
                'who': who,
                'amount': delta,
                'type': action_type
                })
        return {
            'rental_id': self.rental.id,
            'id': self.id,
            'actions': action_deltas
        }
