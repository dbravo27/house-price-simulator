import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from house_price_app.models import House

load_dotenv()

# Load the JSON data
with open("infocasas.json", "r") as f:
    data = json.load(f)

# Set up the database connection
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
DATABASE_URL = f"postgresql://{db_user}:{db_password}@localhost/{db_name}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Insert the data into the database
for item in data:
    house = House(**item)
    session.add(house)
session.commit()
