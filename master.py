import threading
import datetime
import socket
import time
from functools import reduce
from dateutil import parser

# store client address and clock data
client_data = {}

def startRecievingClockTime(connector, address):
    """
    Recieve clock time from connected client.
    Nested thread function.
    """
    while True:
        clock_time_str = connector.recv(1024).decode()
        clock_time = parser.parse(clock_time_str)
        clock_time_diff = datetime.datetime.now() - clock_time

        client_data[address] = {
            'clock_time': clock_time,
            'clock_time_difference': clock_time_diff,
            'connector': connector
        }
        print("Recieved clock time from client: " + str(address) + " at " + str(clock_time))
        time.sleep(7)

def startConnection(master_server):
    """
    Open portal for connecting clients over given port
    """
    # fetch clock time at slaves / clients
    while True:
        # accept a client clock client
        master_slave_connector, address = master_server.accept()
        slave_address = str(address[0]) + ":" + str(address[1])
        print("Connected to client: " + slave_address + "successfully")

        current_thread = threading.Thread( 
						target = startRecievingClockTime, 
						args = (master_slave_connector, slave_address, )) 
        current_thread.start() 

def getAverageClockDiff(): 
    """
    Subroutine function to get average clock difference from all connected clients
    """
    current_client_data = client_data.copy() 

    time_difference_list = list(client['time_difference'] for client_address, client in client_data.items()) 
                                    

    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta(0, 0)) 

    average_clock_difference = sum_of_clock_difference / len(client_data) 

    return average_clock_difference 


def synchronizeAllClocks():
    """
    Master sync thread function to generate 
	cycles of clock synchronization in the network
    """

    while True: 

        print("New synchroniztion cycle started.") 
        print("Number of clients to be synchronized: " + str(len(client_data))) 

        if len(client_data) > 0: 

            average_clock_difference = getAverageClockDiff() 

            for client_addr, client in client_data.items(): 
                try: 
                    synchronized_time = datetime.datetime.now() + average_clock_difference 

                    client['connector'].send(str(synchronized_time).encode()) 

                except Exception as e: 
                    print("Something went wrong while " + "sending synchronized time " + "through " + str(client_addr)) 

        else : 
            print("No client data." + " Synchronization not applicable.") 

        print("\n\n") 

        time.sleep(5) 

def initiateClockServer(port = 8080):
    """
    Initiate clock server / master node
    """
    master_server = socket.socket() 
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    print("Socket at master node created successfully\n") 
        
    master_server.bind(('', port)) 

    # Start listening to requests 
    master_server.listen(10) 
    print("Clock server started...\n") 

    # start making connections 
    print("Starting to make connections...\n") 
    master_thread = threading.Thread(target = startConnection, args = (master_server, )) 
    master_thread.start() 

    # start synchroniztion 
    print("Starting synchronization parallely...\n") 
    sync_thread = threading.Thread(target = synchronizeAllClocks, args = ()) 
    sync_thread.start() 

if __name__ == '__main__': 
	initiateClockServer(port = 8080) 