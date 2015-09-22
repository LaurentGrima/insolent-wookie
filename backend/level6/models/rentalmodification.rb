require_relative 'rental'

# A class managing rental modifications.
#
# Attributes:
#  id (int)
#  rental (Rental): the rental being modified.
#  optional_params: a hash containing optional attributes:
#    start_date (date, optional): Rental modified start date.
#    end_date (date, optional): Rental modified end date.
#    distance (int, optional): Rental modified distance.
class RentalModification
  attr_reader :id
  attr_accessor :rental, :start_date, :end_date, :distance

  def initialize(id, rental, optional_params)
    @id = id
    @rental = rental
    @start_date = optional_params.fetch(:start_date, rental.start_date)
    @end_date = optional_params.fetch(:end_date, rental.end_date)
    @distance = optional_params.fetch(:distance, rental.distance)
  end

  # Computes cost deltas from rental modifications.
  def compute_delta
    # Make a copy of the original rental to compute delta.
    modified_rental = rental.clone
    modified_rental.start_date = start_date
    modified_rental.end_date = end_date
    modified_rental.distance = distance

    # Make a toggler for 'debit' and 'credit':
    # toggle_action_type['debit'] returns 'credit'.
    toggle_action_type = {'debit' => 'credit', 'credit' => 'debit'}

    # Compute delta between the two actions lists.
    action_deltas = []
    rental.get_actions.zip(modified_rental.get_actions).each do |modified_action, action|
      action_type = action[:type]
      who = action[:who]
      delta = action[:amount] - modified_action[:amount]
      if delta < 0
        delta = delta.abs
        action_type = toggle_action_type[action_type]
      end
      action_deltas << {
        :who => who,
        :amount => delta,
        :type => action_type
      }
    end
    {
      :rental_id => rental.id,
      :id => id,
      :actions => action_deltas
    }
  end
end
