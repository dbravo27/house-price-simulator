import json
import os

import django
from django.db import connection

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "house_price_simulator_project.settings"
)
django.setup()

from house_price_app.models import House


def load_json_data(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    for item in data:
        house = House(**item)
        house.save()


json_files = [
    "uruguay_property_scraping/infocasasapartamentos.json",
    "uruguay_property_scraping/infocasascasas.json",
    "uruguay_property_scraping/gallitoapartamentos.json",
    "uruguay_property_scraping/gallitocasas.json",
]

# Clear the house table
House.objects.all().delete()

# Load JSON data from each file
for file_path in json_files:
    load_json_data(file_path)

# Update the prices and currency in the house table
with connection.cursor() as cursor:
    update_query = """
    UPDATE house
    SET price = CASE
        WHEN currency = '$' OR currency = '$U' THEN price/39
        ELSE price
    END,
    currency = 'U$S';
    """

    cursor.execute(update_query)

# Delete temporal rents
with connection.cursor() as cursor:
    update_query = """DELETE FROM house WHERE price < 250;"""

    cursor.execute(update_query)


# Delete temporal rents
with connection.cursor() as cursor:
    update_query = """DELETE FROM house WHERE price > 9999;"""

    cursor.execute(update_query)

# lowercase and no tildes
with connection.cursor() as cursor:
    update_query = """UPDATE house
SET 
    category = lower(unaccent(category)),
    barrio = lower(unaccent(barrio))
    departamento = lower(unaccent(departamento));
"""

    cursor.execute(update_query)

with connection.cursor() as cursor:
    update_query = """
    DELETE FROM table_name
    WHERE square_meters ~ '[A-Za-z]' OR trim(square_meters) = '' OR square_meters ~ '[0-9]+ [A-Za-z]+';

   

    ALTER TABLE house
    ALTER COLUMN square_meters TYPE integer USING square_meters::integer;"""

    cursor.execute(update_query)

with connection.cursor() as cursor:
    update_query = update_query = """
    ALTER TABLE house
    ALTER COLUMN square_meters TYPE integer USING square_meters::integer;"""

    

with connection.cursor() as cursor:
    update_query ="""
    DELETE FROM house
    WHERE (square_meters * 30) < price;"""
    cursor.execute(update_query)