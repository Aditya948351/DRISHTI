import json

with open('DrishtiPlatform/accounts/fixtures/initial_data.json', 'r') as f:
    data = json.load(f)

filtered_data = [
    user for user in data 
    if user['fields'].get('role') != 'citizen'
]

with open('DrishtiPlatform/accounts/fixtures/initial_data_officers.json', 'w') as f:
    json.dump(filtered_data, f, indent=2)

print(f"Filtered {len(data)} users down to {len(filtered_data)} officers/admins.")
