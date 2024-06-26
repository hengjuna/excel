import json

def get_country_name(code):
    # Load the JSON file
    with open('world.zh.json') as f:
        data = json.load(f)

    # Create a dictionary to map iso_a2 to full_name
    country_dict = {}
    for feature in data['features']:
        iso_a2 = feature['properties']['iso_a2']
        name = feature['properties']['name']
        country_dict[iso_a2] = name

    if country_dict.__contains__(code):
        result = country_dict.get(code)
        if len(result) > 4:
            raise Exception("more than 4")
        return country_dict.get(code)


    raise Exception("no name error")
