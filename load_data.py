import json
import os

import django
from django.conf import settings
from dotenv import load_dotenv
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "house_price_simulator_project.settings"
)
django.setup()

# settings.configure(**project_settings.__dict__)

from house_price_app.models import House

load_dotenv()

# Load the JSON data
with open("uruguay_property_scraping/infocasas.json", "r") as f:
    data = json.load(f)

# Set up the database connection
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
DATABASE_URL = f"postgresql://{db_user}:{db_password}@localhost/{db_name}"

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class House(Base):
    __tablename__ = "house"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(20))
    barrio = Column(String(100))
    departamento = Column(String(50))
    square_meters = Column(String(20))
    bedrooms = Column(String(20))
    bathrooms = Column(String(20))
    price = Column(Integer)
    currency = Column(String(20))
    full_link = Column(String(500))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insert the data into the database
for item in data:
    house = House(**item)
    session.add(house)
session.commit()
