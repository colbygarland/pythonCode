README for the messenger lab for CS3130.
--
--
Author: Colby Garland
ID#   : 5034957
--
--
Purpose: Emulate a chatroom, where users can send short messages to each other.
--
--
Git URL: https://github.com/colbygarland/cs3130
--
--
Project is under the "messenger" directory in the git repository above.
--
--
--
Weaknesses:
	1. Sends messages, but treats every user as if they are offline
               ie. saves the messages into a file for later consumption
        2. Messages sent to users can only be one word
--
--
To run the server: type "python3 messenger.py server <ip address of machine>"
To run the client: type "python3 messenger.py client <ip address of machine>" 
--
--
