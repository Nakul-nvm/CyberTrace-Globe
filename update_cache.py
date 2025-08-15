# File: update_cache.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from your .env file

API_KEY = os.getenv('ABUSEIPDB_API_KEY')
CACHE_FILE = 'cache.json'

def refresh_cache():
    if not API_KEY:
        print("Error: ABUSEIPDB_API_KEY not found in .env file.")
        return

    print("Fetching live data to update cache...")
    
    # Fetch from AbuseIPDB
    blacklist_url = 'https://api.abuseipdb.com/api/v2/blacklist'
    params = {'confidenceMinimum': 90, 'limit': 100} # Get a big list
    headers = {'Accept': 'application/json', 'Key': API_KEY}
    
    try:
        response = requests.get(url=blacklist_url, headers=headers, params=params)
        response.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)
        data = response.json()['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from AbuseIPDB: {e}")
        return

    # Geolocate each IP and format the results
    attacks_with_locations = []
    for report in data:
        ip_address = report['ipAddress']
        try:
            geo_response = requests.get(f"http://ip-api.com/json/{ip_address}")
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            if geo_data['status'] == 'success':
                attacks_with_locations.append({
                    "ip": ip_address,
                    "score": report['abuseConfidenceScore'],
                    "lat": geo_data['lat'],
                    "lon": geo_data['lon'],
                    "country": geo_data['country']
                })
        except requests.exceptions.RequestException as e:
            print(f"Could not geolocate IP {ip_address}: {e}")
            continue

    # Save the results to our cache file
    with open(CACHE_FILE, 'w') as f:
        json.dump(attacks_with_locations, f, indent=2)
        print(f"Successfully updated {CACHE_FILE} with {len(attacks_with_locations)} new entries.")

if __name__ == "__main__":
    refresh_cache()