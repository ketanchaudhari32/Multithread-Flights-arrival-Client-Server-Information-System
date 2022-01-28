import requests
import json

params = {
    'access_key': '955ff9aa2c5960c374ce8efea04ecef5',
    }

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()


for flights in api_response['data']:
    #print(flights["flight_status"])
    #print('\n')
    if flights["flight_status"]=="landed":
        print('t')