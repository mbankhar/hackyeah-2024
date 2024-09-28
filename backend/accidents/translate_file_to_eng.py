import json

# A dictionary to map Polish keys to English keys
key_translation = {
    "wsp_gps_x": "gps_x",
    "wsp_gps_y": "gps_y",
    "id_w_czas": "date",
    "czas_zdarzenia": "time",
    "woj_nazwa": "province_name",
    "pow_nazwa": "county_name",
    "gmi_nazwa": "municipality_name",
    "mie_nazwa": "place_name",
    "opis_zdarzenia": "event_description",
    "uczestnicy": "participants",
    "ofiary": "victims",
    "Kierujący": "Driver",
    "Pasażer": "Passenger",
    "obrazenia": "injuries",
    "opis_pojazdu": "vehicle_description",
    "zdarzenie_id": "event_id",
    "id_systemu_zr": "system_id",
    "Brak obrażeń": "No injuries",
    "Lekko": "Minor",
    "Ciężko": "Severe",
    "Motocykl o poj. do 125 cm3 ( do 11 kw/0,1 KW/kg)": "Motorcycle up to 125 cc (up to 11 kw/0.1 KW/kg)",
    "Motocykl inny": "Other motorcycle",
    "Samochód osobowy": "Passenger car",
    "Samochód ciężarowy DMC do 3,5 T": "Truck up to 3.5 T GVW",
    "Samochód ciężarowy DMC powyżej 3,5 T": "Truck over 3.5 T GVW",
    "Tramwaj, trolejbus": "Tram, trolleybus",
    "Rower": "Bicycle",
    "Nie dotyczy": "Not applicable",
    "Inne": "Other"
}

# Function to translate keys using hardcoded values
def translate_keys(data):
    if isinstance(data, dict):
        translated_data = {}
        for key, value in data.items():
            # Translate the key if available in the translation dictionary
            translated_key = key_translation.get(key, key)
            # Recursively translate nested dictionaries
            translated_data[translated_key] = translate_keys(value)
        return translated_data
    elif isinstance(data, list):
        return [translate_keys(item) for item in data]
    else:
        # Translate values only if they match in the dictionary
        return key_translation.get(data, data)

# Function to process the file
def translate_file(input_file, output_file):
    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Translate the JSON data
    translated_data = translate_keys(data)

    # Write the translated data to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=4)
