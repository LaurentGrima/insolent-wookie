require "date"

# A class for rental management.
class Rental
  attr_reader :id
  attr_accessor :car, :start_date, :end_date, :distance
  DECREASE = [
    {:rate => 0.5, :threshold => 10},
    {:rate => 0.7, :threshold => 4},
    {:rate => 0.9, :threshold => 1},
  ]
  COMMISSION_RATE = 0.3
  def initialize(id, car, start_date, end_date, distance)
    @id = id
    @car = car
    @start_date = start_date
    @end_date = end_date
    @distance = distance
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
end
