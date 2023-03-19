import json

# Load the JSON file
with open("uruguay_property_scraping/infocasas.json", "r") as f:
    data = json.load(f)

# Convert string values to integers
for item in data:
    item["square_meters"] = item["square_meters"]
    item["bedrooms"] = item["bedrooms"]
    item["bathrooms"] = item["bathrooms"]
    item["price"] = int(float(item["price"]) * 1000)

# Save the modified JSON back to the file
with open("uruguay_property_scraping/infocasas.json", "w") as f:
    json.dump(data, f, indent=4)
