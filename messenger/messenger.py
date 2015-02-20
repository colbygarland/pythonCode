#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter02/udp_remote.py
# UDP client and server for talking over the network

import argparse, random, socket, sys, main 

MAX_BYTES = 65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')

        print('The client at {} says {!r}'.format(address, text))
        command = text
        txtMessage = ''

        if text.isalpha() == True:
            pass
        else:
            try:
                command, name, txtMessage = text.split(" ", 2)
            except ValueError:
                try:
                    command, name = text.split(" ", 1)
                except:
                    print("Invalid command")


       # SIGNIN COMMAND
        if command == "signin":
            print("command = " + command)
            # searches to see if person is in the system
            inDatabase = logOn(name)
            if inDatabase == True:
                message = "Welcome to the chatroom, " + name + "\n"
                # set the status to online               
                setStatusOn(name)

                inFile = open("messages", "r")
                for rec in inFile:
                    username, msg = rec.split(":", 1)
                    if username == name:
                        message += msg
                inFile.close()

                searchString = name + ":"
                with open("messages", "r+") as inoutfile:
                    lines = [line.replace(searchString, '') for line in inoutfile]
                    inoutfile.seek(0)
                    inoutfile.truncate()
                    inoutfile.writelines(lines)


            else:
                message = name + " is not authorized to be in the chatroom"

       # SIGNOFF COMMAND
        elif command == "signout":
            print("command = " + command)
            inDatabase = logOn(name)
            if inDatabase == True:
                setStatusOff(name)
                message = "GoodBye"
            else:
                message = name + " is not authorized to be in the chatroom"

       # WHOISON COMMAND
        elif command == "whoison":
            listOfNames = whoIsOn()
            length = len(listOfNames)
            message = ""
            
            for i in listOfNames:
                message = message + i

            if length == 0:
                message = "Nobody is currently signed on."

       # SEND COMMAND
        elif command == "send":
            # sees if user is in database
            inDatabase = logOn(name)
            if inDatabase == True:
                # sees if user is currently online
                listOfUsers = whoIsOn()
                listOfNames = []

                for i in listOfUsers:
                    status, listOfNames = i.split(":")

                for rec in listOfNames:
                    if rec == name:
                        message = txtMessage
                        break
                # store message for later consumption
                inFile = open('messages', 'a')
                inFile.write(name + ":" + txtMessage + "\n")
                inFile.close()
                message = 'User not online, saved message for later'
            else:

                message = "User is not in database - SEND 303"
        elif command == '':
            sys.exit(0)
        else:
            print("Unrecognized command")
        
        try:
            sock.sendto(message.encode('ascii'), address)
        except UnboundLocalError:
            print("User didn't enter correct command")
            message = "Command not recognized"


def client(hostname, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))

    conditionSetter = 0

    # Print the main screen
    main.beginningScreen()
  
    while True:  
 
        print("> ", end="")
        text = input()
        text = text.lower()

        if text.isalpha() == True:
            command = ''
            pass
        else:
            try:
                command, name = text.split(" ", 1)
            except ValueError:
                print("User entered incorrect command")

        delay = 0.1 # seconds
        data = text.encode('ascii')

        while True:
            sock.send(data)
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES)
            except (ConnectionRefusedError, socket.timeout):
                print("Server currently not up")
                sys.exit(0)
            else:
                break # we are done, and can stop looping
        print(data.decode('ascii'))

        if command == 'signout':
            break



# logOn(name) checks with the name passed to it to see if user
# is in the database or not
def logOn(name):
    
    inFile = open("database", "r")
    inDatabase = False

    for rec in inFile:
        status, username = rec.split(":", 1)
        username, rest = username.split("\n", 1)

        if name == username:
            inDatabase = True
            break
        else:
            inDatabase = False

    inFile.close()
    return inDatabase

# Setstatuson searches for the name and changes the status in
# the database to on instead of off
def setStatusOn(name):

    searchString = "off:" + name
    with open("database", "r+") as inoutfile:
        lines = [line.replace(searchString, "on:" + name) for line in inoutfile]
        inoutfile.seek(0)
        inoutfile.truncate()
        inoutfile.writelines(lines)

# Setstatusoff searches for the name and changes the status in
# the database to off instead of on
def setStatusOff(name):

    searchString = "on:" + name
    with open("database", "r+") as inoutfile:
        lines = [line.replace(searchString, "off:" + name) for line in inoutfile]
        inoutfile.seek(0)
        inoutfile.truncate()
        inoutfile.writelines(lines)

# Prints out all the names that are online!!
def whoIsOn():

    inFile = open("database", "r")
    names = []

    for rec in inFile:
        status, username = rec.split(":", 1)

        if status == "on":
            names.append(rec)

    for rec in names:
        print(rec)

    return names






if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                    ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                                    ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
    help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
