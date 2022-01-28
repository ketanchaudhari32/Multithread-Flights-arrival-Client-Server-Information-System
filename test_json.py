import json

f = open('group_ID.json',)

data = json.load(f)

flights_data = {}
counter = 0
for flights in data["data"]:
    if flights["flight_status"]=="active":
        flights_data.update({counter:{"Flight Code(IATA)": flights["flight"]["iata"],
                             "Departure Airport": flights["departure"]["airport"],
                             "Arrival Time": flights["arrival"]["scheduled"],
                             "Terminal": flights["arrival"]["terminal"],
                             "Gate": flights["arrival"]["gate"],
                             }},)
        counter+=1
        
print(flights_data)
ddd = json.dumps(flights_data, indent = 1)

dddddd= json.loads(ddd)
print(dddddd[0][0])