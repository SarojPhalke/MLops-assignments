import requests

# Define the API endpoint URL
url = "http://127.0.0.1:8001/filter_wines/"

# Define the query parameters
params = {
    "min_quality": 5,
    "max_quality": 7,
    "features": ["alcohol", "pH"]
}

# Send a GET request to the API
response = requests.get(url, params=params)

# Check the status code of the response
if response.status_code == 200:
    # If successful, print the JSON response
    print(response.json())
else:
    # If there is an error, print the error code
    print(f"Error: {response.status_code}")
