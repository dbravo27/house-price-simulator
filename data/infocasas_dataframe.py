import pandas as pd

# Load the data from the JSON file into a Pandas DataFrame
df = pd.read_json("./uruguay_property_scraping/infocasas.json")

# Display the first 20 rows of the DataFrame
print(df.head(20))
