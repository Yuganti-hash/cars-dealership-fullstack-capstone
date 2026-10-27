from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Nissan Motor Co.", "country": "Japan"},
        {"name": "Mercedes", "description": "Mercedes-Benz AG", "country": "Germany"},
        {"name": "Audi", "description": "Audi AG", "country": "Germany"},
        {"name": "Kia", "description": "Kia Corporation", "country": "South Korea"},
        {"name": "Toyota", "description": "Toyota Motor Corporation", "country": "Japan"},
    ]

    car_make_instances = []
    for data in car_make_data:
        make_obj, _ = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"], "country": data["country"]}
        )
        car_make_instances.append(make_obj)

    make_map = {m.name: m for m in car_make_instances}

    # Exactly the 15 car models matching the official Coursera rubric for Task 14/15
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "car_make": make_map["NISSAN"], "dealer_id": 1},
        {"name": "Qashqai", "type": "SUV", "year": 2024, "car_make": make_map["NISSAN"], "dealer_id": 1},
        {"name": "XTRAIL", "type": "SUV", "year": 2024, "car_make": make_map["NISSAN"], "dealer_id": 1},
        {"name": "A-Class", "type": "HATCHBACK", "year": 2023, "car_make": make_map["Mercedes"], "dealer_id": 2},
        {"name": "C-Class", "type": "SEDAN", "year": 2024, "car_make": make_map["Mercedes"], "dealer_id": 2},
        {"name": "E-Class", "type": "SEDAN", "year": 2024, "car_make": make_map["Mercedes"], "dealer_id": 2},
        {"name": "A4", "type": "SEDAN", "year": 2023, "car_make": make_map["Audi"], "dealer_id": 3},
        {"name": "A5", "type": "COUPE", "year": 2024, "car_make": make_map["Audi"], "dealer_id": 3},
        {"name": "A6", "type": "SEDAN", "year": 2024, "car_make": make_map["Audi"], "dealer_id": 3},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "car_make": make_map["Kia"], "dealer_id": 4},
        {"name": "Carnival", "type": "SUV", "year": 2024, "car_make": make_map["Kia"], "dealer_id": 4},
        {"name": "Cerato", "type": "SEDAN", "year": 2024, "car_make": make_map["Kia"], "dealer_id": 4},
        {"name": "Corolla", "type": "SEDAN", "year": 2023, "car_make": make_map["Toyota"], "dealer_id": 8},
        {"name": "Camry", "type": "SEDAN", "year": 2024, "car_make": make_map["Toyota"], "dealer_id": 8},
        {"name": "Kluger", "type": "SUV", "year": 2024, "car_make": make_map["Toyota"], "dealer_id": 8},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=data["car_make"],
            defaults={"type": data["type"], "year": data["year"], "dealer_id": data["dealer_id"]}
        )

    print("CarMake and CarModel database population completed successfully with 15 models.")
