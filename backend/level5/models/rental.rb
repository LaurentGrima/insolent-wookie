require "date"

# A class for rental management.
#
# Attributes:
#   id (int)
#   car (Car): a Car instance.
#   start_date (date): Rental start date.
#   end_date (date): Rental end date.
#   distance (int): distance diven (km) expected for th rental period.
#   deductible_reduction (boolean): Option for the driver to reduce
#     the deductible amount from €800 to €150,
#     for a few more euros per day.
#   DECREASE (array[Hash]): Holds rates for price per day discounts
#     and duration threshold.
#     The threshold is the minimum duration at which the rate applies.
#     The final rate is 'decrease rate' * 'origin cost per day'.
#   COMMISSION_RATE (float): The rate used to calculate the commission.
#   DEDUCTIBLE_DAILY_FEE (int): The daily rate in case the deductible option is chosen.
class Rental
  attr_reader :id
  attr_accessor :car, :start_date, :end_date, :distance, :deductible_reduction

  DECREASE = [
    {:rate => 0.5, :threshold => 10},
    {:rate => 0.7, :threshold => 4},
    {:rate => 0.9, :threshold => 1},
  ]
  COMMISSION_RATE = 0.3
  DEDUCTIBLE_DAILY_FEE = 400

  def initialize(id, car, start_date, end_date, distance, deductible_reduction)
    @id = id
    @car = car
    @start_date = start_date
    @end_date = end_date
    @distance = distance
    @deductible_reduction = deductible_reduction
  end

  # Calculates the rental duration in days.
  # Example: a rental starting and finishing the same date
  #   has a duration of 1 day.
  # Returns:
  #   The duration as an integer.
  public
  def get_duration
    d1 = DateTime.strptime(start_date, "%Y-%m-%d")
    d2 = DateTime.strptime(end_date, "%Y-%m-%d")
    ((d2 - d1).to_i).abs + 1
  end

  # Calculates the deductible reduction cost if applicable.

  # Returns:
  #   The cost as an integer (0 if the deductible_reduction reduction
  #       was not chosen).
  public
  def get_deductible_reduction
    if deductible_reduction
      return get_duration * DEDUCTIBLE_DAILY_FEE
    else
      return 0
    end
  end

  # Get the options chosen for this rental.
  public
  def options
    {:deductible_reduction => get_deductible_reduction}
  end

  # Calculates the rental total price.
  # Rules apply as follows:
  # New rules:
  #     - price per day decreases by 0.10 after 1 day
  #     - price per day decreases by 0.30 after 4 days
  #     - price per day decreases by 0.50 after 10 days
  # Returns:
  #   The price as an integer.
  public
  def get_price
    duration = get_duration
    diff1 = [duration - DECREASE[0][:threshold], 0].max
    diff2 = [duration - diff1 - DECREASE[1][:threshold], 0].max
    diff3 = [duration - diff1 - diff2 - DECREASE[2][:threshold], 0].max
    total_price_per_day = (
        DECREASE[0][:rate] * diff1 +
        DECREASE[1][:rate] * diff2 +
        DECREASE[2][:rate] * diff3 +
        1) * car.price_per_day
    total_price_per_km = distance * car.price_per_km
    (total_price_per_day + total_price_per_km).round
  end

  # Calculates the commission.
  # Returns:
  #  A hash containing the differents fees.
  public
  def get_commission
    price = get_price
    commission_total = price * COMMISSION_RATE
    insurance_fee = commission_total / 2
    assistance_fee = get_duration * 100
    drivy_fee = [commission_total - (insurance_fee + assistance_fee), 0].max
    {
      :insurance_fee => insurance_fee.round,
      :assistance_fee => assistance_fee.round,
      :drivy_fee => drivy_fee.round
    }
  end

  # Shows how much money must be debited/credited for each actor.
  public
  def get_actions
    commission = get_commission
    deductible_reduction = get_deductible_reduction
    [
      {
        :who => "driver",
        :type => "debit",
        :amount => get_price + deductible_reduction
      },
      {
        :who => "owner",
        :type => "credit",
        :amount => get_price - commission.values.inject(:+)
      },
      {
        :who => "insurance",
        :type => "credit",
        :amount => commission[:insurance_fee]
      },
      {
        :who => "assistance",
        :type => "credit",
        :amount => commission[:assistance_fee]
      },
      {
        :who => "drivy",
        :type => "credit",
        :amount => commission[:drivy_fee] + deductible_reduction
      }
    ]
  end

end
