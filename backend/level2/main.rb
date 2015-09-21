require "json"
require_relative "models/car"
require_relative "models/rental"

file = File.read('data.json')
input_data = JSON.parse(file)

# Create a car hash from input data to access cars by id.
cars = {}
input_data['cars'].each do |car|
  cars[car['id']] = Car.new(car['id'], car['price_per_day'], car['price_per_km'])
end

# Create the list of rentals to be outputted.
rentals = []
input_data['rentals'].each do |input_rental|

  output_rental = Rental.new(
    input_rental['id'],
    cars[input_rental['car_id']],
    input_rental['start_date'],
    input_rental['end_date'],
    input_rental['distance'],
    )

  item = {
    'id': output_rental.id,
    'price': output_rental.get_price
    }
  rentals << item
end

# Output the json file.
File.open("_output.json", "w") do |f|
  f.write({'rentals' => rentals }.to_json)
end