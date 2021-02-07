import json

CONVERTER = {'gasfired': 'gas(euro/MWh)', 'turbojet': 'kerosine(euro/MWh)'}


def get_payload():
    with open('example_payloads/payload2.json') as f:
        data = json.load(f)
    return data


def get_loads_for_wind_plants(wind_plants: list, required_load: int, wind_percentage: int):
    """
    Calculate optimal loads for wind plants

    :param wind_plants: list of wind plants (dictionary with plant fields)
    :param required_load: required load
    :param wind_percentage:
    :return response:
    :return response:
    """
    response = []
    wind_total_load = 0
    for plant in wind_plants:
        if wind_total_load + plant['pmax'] * plant['efficiency'] * (wind_percentage / 100) >= required_load:
            response.append({'name': plant['name'], 'p': required_load - wind_total_load})
            wind_total_load = required_load
        else:
            response.append({'name': plant['name'], 'p': plant['pmax']})
            wind_total_load += plant['pmax']

    required_load -= wind_total_load
    return response, required_load


def calculate_optimal_loads_and_prices(plants: list, required_load: int):
    """
    Calculate optimal loads and prices for non-wind plants

    :param plants: list of plant (list of dictionaries)
    :param required_load:
    :return plants: modified list of plants (with potential_load field added)
    """
    for plant in plants:
        if required_load < plant['pmin']:
            price = plant['pmin'] * plant['unit_price']
            load = required_load
        elif required_load > plant['pmax']:
            price = plant['pmax'] * plant['unit_price']
            load = plant['pmax']
        else:
            price = required_load * plant['unit_price']
            load = required_load
        plant['potential_load'] = {'load': load, 'price': price, 'real_unit_price': price / load}
    return plants


def get_best_plant_index(plants: list):
    """
    Get the index (in the plants list) of the optimal plant to use in priority

    :param plants: list of plant (list of dictionaries)
    :return index: index of the optimal plant (with lowest real unit price)
    """
    index = 0
    minimum = plants[0]['potential_load']['real_unit_price']
    for i, plant in enumerate(plants):
        if plant['potential_load']['real_unit_price'] < minimum:
            minimum = plant['potential_load']['real_unit_price']
            index = i
    return index


def main():
    data = get_payload()
    required_load = data['load']

    # Prioritizing wind plants because of free use
    wind_plants = [plant for plant in data['powerplants'] if plant['type'] == 'windturbine']
    wind_response, required_load = get_loads_for_wind_plants(wind_plants, required_load, data['fuels']['wind(%)'])
    # Initialize 'response' dictionary of optimal loads with optimal wind loads
    response = [res for res in wind_response]

    # Focusing on non-wind plants
    non_free_plants = [plant for plant in data['powerplants'] if plant['type'] != 'windturbine']

    # Calculate unit price
    for plant in non_free_plants:
        plant['unit_price'] = data['fuels'][CONVERTER[plant['type']]] * plant['efficiency']

    # 1. Calculate optimal load and price for every plant.
    # 2. Choosing the best plant and adding the equivalent load to the final response.
    # 3. Repeat the loop until required load is not filled.
    while (required_load > 0) & (non_free_plants != []):
        non_free_plants = calculate_optimal_loads_and_prices(non_free_plants, required_load)
        best_plant = non_free_plants.pop(get_best_plant_index(non_free_plants))
        response.append({'name': best_plant['name'], 'p': best_plant['potential_load']['load']})
        required_load -= best_plant['potential_load']['load']

    # Adding the last plants to the response (with empty load)
    for plant in non_free_plants:
        response.append({'name': plant['name'], 'p': 0})

    print(required_load)
    print(response)

    with open('response.json', 'w') as outfile:
        json.dump(response, outfile)


if __name__ == '__main__':
    main()

# TODO: Generalize wind plants and other plants. The logic can be generalized in case wind plants use becomes not free
# TODO: Improve structure of the scripts
# TODO: Improve flexibility of types in functions ('int' -> ('float' | 'int') )
# TODO: Do more tests on responses. Is the response the optimal solution?
# TODO: Improve data structures for plants (avoid copy )
