import csv


def search_csv(csv_file, search_column, search_value, result_column, max_results=10):
    found_data = []
    count = 0
    result_id=1
    with open(csv_file, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            column_data = row[search_column]
            if search_value.lower() in column_data.lower():
                # Create a new dictionary with an 'ID' key and its value
                result_dict = dict(row)
                result_dict['id'] = result_id
                found_data.append(result_dict)
                count += 1
                result_id += 1
                if count >= max_results:
                    break
    return found_data