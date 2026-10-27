from .models import CarMake, CarModel

def initiate():
    car_make_data = [
        {"name": "Audi", "description": "Vorsprung durch Technik - German luxury automaker", "country": "Germany"},
        {"name": "Ford", "description": "Built Ford Tough - American automotive pioneer", "country": "USA"},
        {"name": "Toyota", "description": "Let's Go Places - Renowned for reliability and innovation", "country": "Japan"},
        {"name": "Honda", "description": "The Power of Dreams - Japanese performance and efficiency", "country": "Japan"},
        {"name": "BMW", "description": "The Ultimate Driving Machine - Bavarian automotive excellence", "country": "Germany"},
        {"name": "Nissan", "description": "Innovation that excites - Advanced automotive design", "country": "Japan"},
    ]

    car_make_instances = []
    for data in car_make_data:
        make_obj, _ = CarMake.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"], "country": data["country"]}
        )
        car_make_instances.append(make_obj)

    # Map make name to instance
    make_map = {m.name: m for m in car_make_instances}

    car_model_data = [
        {"name": "A4", "type": "SEDAN", "year": 2023, "car_make": make_map["Audi"], "dealer_id": 1},
        {"name": "A6", "type": "SEDAN", "year": 2024, "car_make": make_map["Audi"], "dealer_id": 1},
        {"name": "Q5", "type": "SUV", "year": 2024, "car_make": make_map["Audi"], "dealer_id": 1},
        {"name": "F-150", "type": "TRUCK", "year": 2024, "car_make": make_map["Ford"], "dealer_id": 1},
        {"name": "Mustang", "type": "COUPE", "year": 2023, "car_make": make_map["Ford"], "dealer_id": 2},
        {"name": "Explorer", "type": "SUV", "year": 2024, "car_make": make_map["Ford"], "dealer_id": 3},
        {"name": "Camry", "type": "SEDAN", "year": 2023, "car_make": make_map["Toyota"], "dealer_id": 1},
        {"name": "Corolla", "type": "SEDAN", "year": 2024, "car_make": make_map["Toyota"], "dealer_id": 2},
        {"name": "RAV4", "type": "SUV", "year": 2024, "car_make": make_map["Toyota"], "dealer_id": 3},
        {"name": "Civic", "type": "SEDAN", "year": 2023, "car_make": make_map["Honda"], "dealer_id": 2},
        {"name": "Accord", "type": "SEDAN", "year": 2024, "car_make": make_map["Honda"], "dealer_id": 2},
        {"name": "CR-V", "type": "SUV", "year": 2024, "car_make": make_map["Honda"], "dealer_id": 1},
        {"name": "3 Series", "type": "SEDAN", "year": 2023, "car_make": make_map["BMW"], "dealer_id": 4},
        {"name": "X5", "type": "SUV", "year": 2024, "car_make": make_map["BMW"], "dealer_id": 5},
        {"name": "Altima", "type": "SEDAN", "year": 2023, "car_make": make_map["Nissan"], "dealer_id": 6},
        {"name": "Rogue", "type": "SUV", "year": 2024, "car_make": make_map["Nissan"], "dealer_id": 7},
    ]

    for data in car_model_data:
        CarModel.objects.get_or_create(
            name=data["name"],
            car_make=data["car_make"],
            year=data["year"],
            defaults={"type": data["type"], "dealer_id": data["dealer_id"]}
        )

    print("CarMake and CarModel database population completed successfully.")
