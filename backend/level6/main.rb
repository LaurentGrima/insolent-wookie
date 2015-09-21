require "json"
require_relative "models/car"
require_relative "models/rental"
require_relative "models/rentalmodification"

file = File.read('data.json')
input_data = JSON.parse(file)

# Create a car hash from input data to access cars by id.
cars = {}
input_data['cars'].each do |car|
  cars[car['id']] = Car.new(car['id'], car['price_per_day'], car['price_per_km'])
end

# Create rental hash to access rentals by id.
rentals = {}
input_data['rentals'].each do |input_rental|
  output_rental = Rental.new(
    input_rental['id'],
    cars[input_rental['car_id']],
    input_rental['start_date'],
    input_rental['end_date'],
    input_rental['distance'],
    input_rental['deductible_reduction'],
  )
  rentals[output_rental.id] = output_rental
end

# Create the list of modifications to be outputted.
rental_modifications = []
input_data['rental_modifications'].each do |modification|
  optional_params = {}
  optional_params[:start_date] = modification['start_date'] if modification['start_date']
  optional_params[:end_date] = modification['end_date'] if modification['end_date']
  optional_params[:distance] = modification['distance'] if modification['distance']

  output_modification = RentalModification.new(
    modification['id'],
    rentals[modification['rental_id']],
    optional_params
  )
  rental_modifications << output_modification.compute_delta
end

# Output the json file.
File.open("_output.json", "w") do |f|
  f.write({'rental_modifications' => rental_modifications }.to_json)
end