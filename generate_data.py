import json
from datetime import timedelta, datetime
import random
import pyperclip


def generate_sample_data():
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=29)

    data = {}
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime("%m-%d-%Y")

        data[date_str] = {
            "hourly_intake": {}
        }

        for hour in range(24):
            data[date_str]["hourly_intake"][str(hour)] = []

            for _ in range(random.randint(1, 3)):
                food_item = {
                    "name": f"food_{random.randint(1, 10)}",
                    "calories": round(random.uniform(50, 300), 1),
                    "fats": round(random.uniform(1, 20), 1),
                    "proteins": round(random.uniform(1, 20), 1),
                    "carbs": round(random.uniform(1, 50), 1),
                }

                data[date_str]["hourly_intake"][str(hour)].append([food_item])

        current_date += timedelta(days=1)

    return data


if __name__ == "__main__":
    sample_data = generate_sample_data()

    # Save the generated data to a JSON file
    with open("sample_data.json", "w") as json_file:
        json.dump(sample_data, json_file, indent=2)

    # Copy the generated data to the clipboard
    json_string = json.dumps(sample_data, indent=2)
    pyperclip.copy(json_string)

    print("Sample data generated and copied to the clipboard.")
