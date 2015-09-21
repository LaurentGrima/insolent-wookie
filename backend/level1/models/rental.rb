require "date"

# A class for rental management.
class Rental
  attr_reader :id
  attr_accessor :car, :start_date, :end_date, :distance

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
  def get_rental_duration
    d1 = DateTime.strptime(start_date, "%Y-%m-%d")
    d2 = DateTime.strptime(end_date, "%Y-%m-%d")
    ((d2 - d1).to_i).abs + 1
  end

  # Calculates the rental total price.
  # Returns:
  #   The price as an integer.
  public
  def get_price
    get_rental_duration * car.price_per_day + distance * car.price_per_km
  end
end
