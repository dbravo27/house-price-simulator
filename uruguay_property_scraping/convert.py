import json

from unidecode import unidecode


def read_neighborhoods_from_file(filename):
    with open(filename, "r") as file:
        neighborhoods = [line.strip() for line in file.readlines()]
    return neighborhoods


# Load the JSON file
with open("gallitoapartamentos.json", "r") as f:
    data = json.load(f)


for item in data:
    item["category"] = unidecode(item["category"].lower())
    if "barrio" in item:
        item["barrio"] = unidecode(item["barrio"].lower())
    else:
        item["barrio"] = ""

    if "price" in item and isinstance(item["price"], int):
        continue

    if "price" in item and item["price"].strip():
        item["price"] = int(item["price"].replace(".", ""))
    else:
        item["price"] = ""


departamentos = ["montevideo", "maldonado", "canelones", "colonia"]
for departamento in departamentos:
    neighborhoods_file = f"neighborhoods_{departamento}.txt"
    neighborhoods = read_neighborhoods_from_file(neighborhoods_file)

    for item in data:
        if item["departamento"].strip() != "":
            continue  # Skip if 'departamento' is already set

        if item["barrio"] in neighborhoods:
            item["departamento"] = departamento
        else:
            item["departamento"] = ""


# Filter items with non-blank 'price'
filtered_data = [item for item in data if item["price"] != ""]

# Save the modified JSON back to the file
with open("gallitoapartamentos.json", "w") as f:
    json.dump(filtered_data, f, indent=4)
