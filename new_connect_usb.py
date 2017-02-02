'''
    How to use:
    to start with specified host IP and port example ip = 127.0.0.1 port 8270 - "python connect_usb.py 127.0.0.1 8270" or just
    "python connect_usb.py" which will use a default IP = 127.0.0.1 and a port ID of 8270
    to start with the server's IP and specified port 8270 - "python connect_usb.py 0.0.0.0 8270"
    to start with server's port and automatically find an open port and write port number to a file - "python connect_usb.py 0.0.0.0 0 protfile.txt"
    see this for more: https://github.com/robotframework/PythonRemoteServer
    to hard code IP and port change the last line in this file to: RobotRemoteServer(UsbConnection(),host='127.0.0.1', port=8270, *sys.argv[1:])

    to use keywords in robot framework:
    example for usb1: "connect usb    usb1" or "disconnect usb    usb1" the connection IDs usb1 through usb6 will be labeled on the phidget relay boxes.

    John Sayeau
    '''

#phidgets imports
from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import InterfaceKit
from time import sleep as sleep


class ConnectBoard():
    def __init__(self, serial_num):
        self.serial_num = serial_num


    #create an interface kit object - "interface kit" refers to the relay board
    def init_phidget(self):
        try:
            interfaceKit = InterfaceKit()
        except RuntimeError as e:
            print("runtime error: %s" % e.details)
            print ("exiting.....")
            exit(1)


        #Open
        try:
            interfaceKit.openPhidget(self.serial_num)
        except PhidgetException as e:
            print("Phidget exception: %i, %s"% e.code, e.details)
            print("Exiting.....")
            exit(1)


        #wait for phidget to connect
        try:
            interfaceKit.waitForAttach(10000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            try:
                interfaceKit.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))
                print("Exiting....")
                exit(1)
            print("Exiting....")
            exit(1)
        else:
            return interfaceKit


    #phidget documentation recommends closing the phidget connection after use.
    def close_phidget(self, phidget):
        try:
            phidget.closePhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)


    #this function connects usb "1" or "2" and either sets the state 2 "connect" or "disconnect"
    #there are 2 sets of relays connected to the phidget relay board. usb 1 is controlled by relays 0 - 3 and usb2
    #is controlled by relays 4 - 7
    def connection(self, usb, state):
        #initialize phidget
        relay_board = self.init_phidget()
        #setup relays to be used based on usb cable to be used
        if usb == 1:
            relay_range = range(0,4)
        elif usb == 2:
            relay_range = range(4, 8)
        else:
            raise Exception["Invalid USB parameter should be either '1' or '2' "]
            exit(1)
        #set connection state argument
        if state == "connect":
            relay_state = 1
        elif state == "disconnect":
            relay_state = 0
        else:
            raise Exception["state must be either 'connect' or disconnect'"]
            exit(1)
        #set requested relays to connected or disconnected
        for relay in relay_range:
            try:
                relay_board.setOutputState(relay,relay_state)
            except PhidgetException as e:
                print("Phidget exception: %s" % e.details)
                print("Exiting.....")
                exit(1)
        #close off the phidget connection
        self.close_phidget(relay_board)


class ConnectionException(Exception):
    def __init__(self, message):
        self.message = message


class UsbConnection():
    #only place serial numbers in code. change serial here if a board is changed or added
    serial_number_list = [312097, 389665, 389823]
    available_connections = {"usb1":[serial_number_list[0], 1],
                             "usb2":[serial_number_list[0], 2],
                             "usb3":[serial_number_list[1], 1],
                             "usb4":[serial_number_list[1], 2],
                             "usb5":[serial_number_list[2], 1],
                             "usb6":[serial_number_list[2], 2]}

    #This function is not to be used as a keyword for robot framework
    def check_valid_connection(self, usb_connection):
        valid_connection = UsbConnection.available_connections.get(usb_connection, "not valid")
        return valid_connection


    def connect_usb(self, usb_connection):
        '''
        This following function can be used as robot framework keywords
        usage example: "connect usb    usb1"
        '''
        if self.check_valid_connection(usb_connection) != "not valid":
            board_serial = UsbConnection.available_connections[usb_connection][0]
            board_usb_port = UsbConnection.available_connections[usb_connection][1]
            board = ConnectBoard(board_serial)
            board.connection(board_usb_port, "connect")
            del board
        else:
            raise ConnectionException(usb_connection + " is not valid check paidget case labels")

    def disconnect_usb(self, usb_connection):
        '''
        This following function can be used as robot framework keywords
        usage example: "disconnect usb    usb1"
        '''
        if self.check_valid_connection(usb_connection) != "not valid":
            board_serial = UsbConnection.available_connections[usb_connection][0]
            board_usb_port = UsbConnection.available_connections[usb_connection][1]
            board = ConnectBoard(board_serial)
            board.connection(board_usb_port, "disconnect")
            del board
        else:
            raise ConnectionException(usb_connection + " is not valid check phidget case labels")

			
    def loop_connect_disconnect(self, usb_connection, number_of_loops, pause = 1):
        x = 0
        while x < number_of_loops:
            self.connect_usb(usb_connection)
            sleep(pause)
            self.disconnect_usb(usb_connection)
            sleep(pause)
	    x = x + 1

			
if __name__ == '__main__':
    import sys
    from robotremoteserver import RobotRemoteServer
    RobotRemoteServer(UsbConnection(), *sys.argv[1:])







