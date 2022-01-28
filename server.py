# Import modules
import socket               
import requests
import json
import time
from _thread import *

def client_thread(arr_icao, c, addr, api_response):
    #Sending message to connected client
    greet_mess = "Server -> Success connecting to "+arr_icao+" server"
    c.sendall(greet_mess.encode("utf-8"))
    
    #getting username 
    c.sendall("Server -> Enter Username: ".encode("utf-8"))
    username = c.recv(1024).decode()
    
    print("Got connection from {} | Username: {}".format(addr, username))
    
    c.sendall('Server -> Server Menu\nServer -> Enter "1" : Arrived Flight Details\nServer -> Enter "2" : Delayed Flight Details\nServer -> Enter "3" : All flights from a specific city\nServer -> Enter "4" : Details Of Particular Flight\nServer -> Press any key to Exit from server\n'.encode("utf-8"))
    
    c.sendall("Server -> Enter Your Choice: ".encode("utf-8"))
    client_choice = c.recv(1024).decode()
    
    while True:
        #Arrived Flight details
        if client_choice=="1":
            print('Requester Name: {} ||| Type of Request: Arrived Flight details ||| Request Parameters: Flight Code(IATA)|Departure Airport|Arrival Time|Terminal|Gate'.format(username))
            c.sendall("Server -> flight details".encode("utf-8"))
            flights_data = []
            for flights in api_response["data"]:
                if flights["flight_status"]=="active":
                    flights_data.append({"Flight Code(IATA)": flights["flight"]["iata"],
                             "Departure Airport": flights["departure"]["airport"],
                             "Arrival Time": flights["arrival"]["scheduled"],
                             "Terminal": flights["arrival"]["terminal"],
                             "Gate": flights["arrival"]["gate"],
                             })
        
            flights_data = json.dumps(flights_data)
            c.sendall(flights_data.encode())
            
        #Delayed Flight Details
        elif client_choice=="2":
            print('Requester Name: {} ||| Type of Request: Delayed Flight Details ||| Request Parameters: Flight Code(IATA)|Departure Airport|Estimated Arrival Time|Terminal|Gate'.format(username))
            c.sendall("Server -> delayed flight details".encode("utf-8"))
            flights_data = []
            for flights in api_response["data"]:
                if flights["arrival"]["delay"] != None:
                    flights_data.append({"Flight Code(IATA)": flights["flight"]["iata"],
                             "Departure Airport": flights["departure"]["airport"],
                             "Departure Time": flights["departure"]["scheduled"],
                             "Estimated Arrival Time": flights["arrival"]["estimated"],
                             "Terminal": flights["arrival"]["terminal"],
                             "Gate": flights["arrival"]["gate"],
                             })
    

            flights_data = json.dumps(flights_data)
            c.sendall(flights_data.encode())
            
        #All flight from specific city
        elif client_choice=="3":
            print('Requester Name: {} ||| Type of Request: All flight from specific city ||| Request Parameters: Flight Code(IATA)|Departure Airport|Departure Time|Estimated Arrival Time|Terminal|Gate'.format(username))
            c.sendall("Server -> Enter City: ".encode("utf-8"))
            city = c.recv(1024).decode()
            flights_data = []
            for flights in api_response["data"]:
                if flights["departure"]["timezone"] == city:
                    flights_data.append({"Flight Code(IATA)": flights["flight"]["iata"],
                             "Departure Airport": flights["departure"]["airport"],
                             "Departure Time": flights["departure"]["scheduled"],
                             "Estimated Arrival Time": flights["arrival"]["estimated"],
                             "Terminal": flights["arrival"]["terminal"],
                             "Gate": flights["arrival"]["gate"],
                             })

            flights_data = json.dumps(flights_data)
            c.sendall(flights_data.encode())
            
        #Detaills of particular flight
        elif client_choice=="4":
            print('Requester Name: {} ||| Type of Request: Detaills of particular flight ||| Request Parameters: Date|Departure Airport|Departure Time|Departure Terminal|Arrival Airport|Arrival Time|Arrival Terminal|Status|Scheduled Departure Time|Scheduled Arrival Time|Estimated Arrival Time|Delay'.format(username))
            c.sendall("Server -> Enter flight Code: ".encode("utf-8"))
            code = c.recv(1024).decode()
            flights_data = []
            for flights in api_response["data"]:
                if flights["flight"]["iata"] == code:
                    flights_data.append({"Flight Code(IATA)": flights["flight"]["iata"],
                             "Date": flights["flight_date"],
                             "Departure Airport": flights["departure"]["airport"],
                             "Departure Time": flights["departure"]["scheduled"],
                             "Departure Terminal": flights["departure"]["terminal"],
                             "Arrival Airport": flights["arrival"]["airport"],
                             "Arrival Time": flights["arrival"]["scheduled"],
                             "Arrival Terminal": flights["arrival"]["terminal"],
                             "Status": flights["flight_status"],
                             "Scheduled Departure Time": flights["departure"]["scheduled"],
                             "Scheduled Arrival Time": flights["arrival"]["scheduled"],
                             "Estimated Arrival Time": flights["arrival"]["estimated"],
                             "Delay": flights["arrival"]["delay"],
                             })

            flights_data = json.dumps(flights_data)
            c.sendall(flights_data.encode())
            
        #Disconnect
        else:
            # Close client connection
            c.sendall("exit".encode("utf-8"))
            print(username, "Disconnected !!!!")
            c.close()
            break
        c.sendall("Server -> Enter Your Choice: ".encode("utf-8"))
        client_choice = c.recv(1024).decode()

if __name__=="__main__":
    #Getting Airport Code
    arr_icao = input("Enter the Airport Code: ") #Example:KSFO

    print("IMPORTING FLIGHT\"s DATA ......")

    #Retrieve 100 flights"s information
    params = {
    "access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "arr_icao": arr_icao,
    "limit": 100
    }

    api_result = requests.get("http://api.aviationstack.com/v1/flights", params)
    api_response = api_result.json()

    print("IMPORTING SUCESSFULL")

    # Writing to group_ID.json
    with open("group_ID.json", "w") as outfile:
        outfile.write(json.dumps(api_response, indent = 1))
        
    print("Starting Server ........")
    # Create a socket object
    s = socket.socket() 
            
    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service.
    port = 12345  
                
    # Bind to the port
    s.bind((host, port))

    print("Server started sucessfully at ",host)

    # Now wait for client connection.
    s.listen(3)                 
    
    while True:
        # Establish connection with client.    
        c, addr = s.accept()   
        
        start_new_thread(client_thread ,(arr_icao, c, addr, api_response,))
        
        
#close connection
s.close()