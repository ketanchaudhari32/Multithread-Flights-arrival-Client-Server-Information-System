# Import socket module
import socket               
import sys
import json

if __name__=="__main__":
    
    # Create a socket object
    s = socket.socket()
            
    # Get local machine name
    host = socket.gethostname()

    # Reserve a port for your service.
    port = 12345        
    s.connect((host, port)) 
    
    print(s.recv(1024).decode())
    print('\n')
    
    #client username 
    input_user = s.recv(1024).decode()       
    username = input(input_user)
    print('\n')
    
    #send client username to server
    s.sendall(username.encode('utf-8'))
        
    print(s.recv(1024).decode())
    
    user_choice = input(s.recv(1024).decode())       
    s.sendall(user_choice.encode('utf-8'))
            
    while True:
        server_reply = s.recv(1024).decode()
        
        if server_reply =='Server -> flight details':
            data_load = s.recv(102400).decode()
            data = json.loads(data_load)
            if data == []:
                print('No Data Found')
            else:
                print('Flight Code(IATA)|Departure Airport|Arrival Time|Terminal|Gate')
                print('---------------------------------------------------------------')
                for i in data:
                    print(i['Flight Code(IATA)'],"|",i['Departure Airport'],"|",i['Arrival Time'],"|",i['Terminal'],"|",i['Gate'])
            
        if server_reply =='Server -> delayed flight details':
            
            data_load = s.recv(102400).decode()
            data = json.loads(data_load)
            if data == []:
                print('No Data Found')
            else:
                print('Flight Code(IATA)|Departure Airport|Estimated Arrival Time|Terminal|Gate')
                print('------------------------------------------------------------------------')
                for i in data:
                    print(i['Flight Code(IATA)'],"|",i['Departure Airport'],"|",i['Estimated Arrival Time'],"|",i['Terminal'],"|",i['Gate'])
        
        if server_reply =='Server -> Enter City: ':
            city_choice = input(server_reply)       
            s.sendall(city_choice.encode('utf-8'))
            
            data_load = s.recv(102400).decode()
            data = json.loads(data_load)
            if data == []:
                print('No Data Found')
            else:
                print('Flight Code(IATA)|Departure Airport|Departure Time|Estimated Arrival Time|Terminal|Gate')
                print('-----------------------------------------------------------------------------------------')
                for i in data:
                    print(i['Flight Code(IATA)'],"|",i['Departure Airport'],"|",i['Departure Time'],"|",i['Estimated Arrival Time'],"|",i['Terminal'],"|",i['Gate'])
            
        if server_reply =='Server -> Enter flight Code: ':
            flight_code = input(server_reply)       
            s.sendall(flight_code.encode('utf-8'))
            
            data_load = s.recv(102400).decode()
            data = json.loads(data_load)
            if data == []:
                print('No Data Found')
            else:
                print('Date|Departure Airport|Departure Time|Departure Terminal|Arrival Airport|Arrival Time|Arrival Terminal|Status|Scheduled Departure Time|Scheduled Arrival Time|Estimated Arrival Time|Delay')
                print('---------------------------------------------------------------------------------------------------------')
                for i in data:
                    print(i['Date'],"|",i['Departure Airport'],"|",i['Departure Time'],"|",i['Departure Terminal'],
                          "|",i['Arrival Airport'],"|",i['Arrival Terminal'],"|",i['Terminal'],
                          "|",i['Status'],"|",i['Scheduled Departure Time'],"|",i['Scheduled Arrival Time'],"|",i['Estimated Arrival Time'],"|",i['Delay'])
        
        if server_reply=='exit':
            sys.exit(0)
            s.close()
            
        print('\n')
        user_choice = input(s.recv(1024).decode())       
        s.sendall(user_choice.encode('utf-8'))