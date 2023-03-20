import json
import os

import django
from django.db import connection

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "house_price_simulator_project.settings"
)
django.setup()

from house_price_app.models import House

# Load the JSON data
with open("uruguay_property_scraping/infocasasapartamentos.json", "r") as f:
    data = json.load(f)

# # Clear the house table
# House.objects.all().delete()

# Insert the data into the database
for item in data:
    house = House(**item)
    house.save()

# Update the prices and currency in the house table
with connection.cursor() as cursor:
    update_query = """
    UPDATE house
    SET price = CASE
        WHEN currency = '$' THEN price/39
        ELSE price
    END,
    currency = 'U$S'
    WHERE currency = '$';
    """

    cursor.execute(update_query)

# Delete temporal rents
with connection.cursor() as cursor:
    update_query = """DELETE FROM house WHERE price < 250;"""

    cursor.execute(update_query)
