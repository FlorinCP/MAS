import json

# Sample data for hospitals, fire stations, police stations, and rescuers (as a separate section)
resources = {
    "hospitals": [
        {
            "id": "hospital_1",
            "x_coordinate": 41.6580000,
            "y_coordinate": -0.8600000,
            "beds_available": 50,
            "specialties": ["emergency", "trauma", "surgery"],
            "status": "operational"
        },
        {
            "id": "hospital_2",
            "x_coordinate": 41.6590000,
            "y_coordinate": -0.8610000,
            "beds_available": 30,
            "specialties": ["pediatrics", "orthopedics", "intensive care"],
            "status": "operational"
        }
    ],
    "fire_stations": [
        {
            "id": "fire_station_1",
            "x_coordinate": 41.6578495,
            "y_coordinate": -0.8590473,
            "type": "rescue",
            "capacity": 6,
            "equipment": ["firehose", "extinguisher", "cutting tool"],
            "status": "on_scene"
        },
        {
            "id": "fire_station_2",
            "x_coordinate": 41.6598495,
            "y_coordinate": -0.8610473,
            "type": "ladder",
            "capacity": 4,
            "equipment": ["ladder", "firehose"],
            "status": "available"
        }
    ],
    "police_stations": [
        {
            "id": "police_station_1",
            "x_coordinate": 41.6600000,
            "y_coordinate": -0.8605000,
            "officers_on_duty": 12,
            "specialties": ["patrol", "crime prevention", "investigation"],
            "status": "operational"
        },
        {
            "id": "police_station_2",
            "x_coordinate": 41.6610000,
            "y_coordinate": -0.8608000,
            "officers_on_duty": 8,
            "specialties": ["patrol", "investigation"],
            "status": "operational"
        }
    ],
    "rescuers": [  # Separate section for rescuers
        {
            "id": "rescuer_1",
            "role": "paramedic",
            "fire_station_id": "fire_station_1",  # Reference to the fire station
            "x_coordinate": 41.6585000,
            "y_coordinate": -0.8603000,
            "equipment": ["defibrillator", "first aid kit", "oxygen tank"],
            "status": "available"
        },
        {
            "id": "rescuer_2",
            "role": "firefighter",
            "fire_station_id": "fire_station_1",  # Reference to the fire station
            "x_coordinate": 41.6602000,
            "y_coordinate": -0.8609000,
            "equipment": ["firehose", "fireproof suit", "ax"],
            "status": "on_scene"
        },
        {
            "id": "rescuer_3",
            "role": "firefighter",
            "fire_station_id": "fire_station_2",  # Reference to the fire station
            "x_coordinate": 41.6610000,
            "y_coordinate": -0.8605000,
            "equipment": ["firehose", "fireproof suit", "ladder"],
            "status": "available"
        }
    ]
}

# Function to write data to a JSON file
def write_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Save the resources to individual JSON files
write_to_json(resources['hospitals'], 'hospitals.json')
write_to_json(resources['fire_stations'], 'fire_stations.json')
write_to_json(resources['police_stations'], 'police_stations.json')
write_to_json(resources['rescuers'], 'rescuers.json')  # Saving the rescuers data

print("JSON files created successfully!")
