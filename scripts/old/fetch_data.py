import requests
import json

url = "https://devops.nighthawkcodingsociety.com/api/users/2025"

# Fetch data from API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Save data to JSON file
    with open('data_dump.json', 'w') as json_file:
        json.dump(data, json_file)
else:
    print(f"Failed to fetch data: {response.status_code}")
