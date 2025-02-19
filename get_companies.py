import requests
import pandas as pd
import json
from config import SAM_GOV_API_KEY  # Import API key from config.py

# Correct SAM.gov API endpoint
URL = "https://api.sam.gov/entity-information/v4/entities"

# API query parameters
params = {
    "q": "TX",  # Filter for Texas companies
    "api_key": SAM_GOV_API_KEY,
    "size": 10  # Adjust as needed
}

# Request data from API
response = requests.get(URL, params=params)

# Check response status
if response.status_code != 200:
    print(f"Error: API request failed with status {response.status_code}")
    print("Response:", response.text[:500])  # Print a snippet for debugging
    exit(1)

# Try to parse JSON response
try:
    data = response.json()
    # Save response JSON to a text file
    with open("data/sam_response.txt", "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4))  # Pretty print JSON
    print("API response saved to data/sam_response.txt")
except requests.exceptions.JSONDecodeError:
    print("Error: Response is not a valid JSON.")
    exit(1)

# Extract required fields
companies = []
for entity in data.get("entityData", []):  # Use 'entityData' instead of 'entities'
    registration = entity.get("entityRegistration", {})
    points_of_contact = entity.get("pointsOfContact", {})

    # Government POC
    gov_poc = points_of_contact.get("governmentBusinessPOC", {})
    gov_poc_name = f"{gov_poc.get('firstName', '')} {gov_poc.get('lastName', '')}".strip()
    gov_poc_title = gov_poc.get("title", "N/A")

    # Electronic Business POC
    e_poc = points_of_contact.get("electronicBusinessPOC", {})
    e_poc_name = f"{e_poc.get('firstName', '')} {e_poc.get('lastName', '')}".strip()
    e_poc_title = e_poc.get("title", "N/A")

    companies.append({
        "Legal Business Name": registration.get("legalBusinessName", "N/A"),
        "DBA Name": registration.get("dbaName", "N/A"),
        "DUNS": registration.get("dodaac", "N/A"),  # DUNS is not provided, using 'dodaac' instead
        "Government POC": gov_poc_name,
        "Government POC Title": gov_poc_title,
        "Electronic Business POC": e_poc_name,
        "Electronic Business POC Title": e_poc_title
    })

# Convert to DataFrame and save
df_companies = pd.DataFrame(companies)
df_companies.to_csv("data/sam_texas_companies.csv", index=False)

print(f"Saved {len(companies)} Texas company records to data/sam_texas_companies.csv")
