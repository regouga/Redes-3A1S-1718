#!/usr/bin/env python

import socket
import sys
import os
import signal

aux = 0

BUFFER_SIZE = 1024 

def signal_handler(signal, frame):
		exitMessage = "\nUNR " + str(UDP_IP) + ' ' + str(TCP_PORT) + "\n"
		print exitMessage
		sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sockUDP.sendto(exitMessage, (UDP_IP, UDP_PORT))
		sockUDP.close()

		sys.exit(0)


sizeof = len(sys.argv)

if sys.argv[1] == "-e" or sys.argv[1] == "-p" or sys.argv[1] == "-n":
	print "Invalid syntax. Please try again."
	sys.exit(0)


elif sizeof > 6 and sys.argv[-2] == "-e" and sys.argv[-4] == "-n" and sys.argv[-6] == "-p":
	UDP_PORT = sys.argv[-1]
	UDP_IP = sys.argv[-3] + '.tecnico.ulisboa.pt'
	TCP_IP = sys.argv[-3] + '.tecnico.ulisboa.pt'
	TCP_PORT = sys.argv[-5]

	aux = 7

elif sizeof > 1 and not sys.argv[-2] == "-e" and not sys.argv[-4] == "-n" and not sys.argv[-6] == "-p":
	UDP_PORT = 58067
	UDP_IP = str(socket.gethostname())
	TCP_IP = str(socket.gethostname())
	TCP_PORT = 59000

	aux = 1


elif sizeof > 4 and sys.argv[-2] == "-n" and sys.argv[-4] == "-p":
	UDP_PORT = 58067
	UDP_IP = sys.argv[-1] + '.tecnico.ulisboa.pt'
	TCP_IP = sys.argv[-1] + '.tecnico.ulisboa.pt'
	TCP_PORT = sys.argv[-3]

	aux = 5

elif sizeof > 4 and sys.argv[-2] == "-e" and sys.argv[-4] == "-p":
	UDP_PORT = int(sys.argv[-1])
	UDP_IP = str(socket.gethostname())
	TCP_IP = str(socket.gethostname())
	TCP_PORT = int(sys.argv[-3])

	aux = 5

elif sizeof > 4 and sys.argv[-4] == "-n" and sys.argv[-2] == "-e":
	UDP_PORT = sys.argv[-1]
	UDP_IP = sys.argv[-3]
	TCP_IP = sys.argv[-3]
	TCP_PORT = 59000

	aux = 5

elif sizeof > 2 and sys.argv[-2] == "-p":
	UDP_PORT = 58067
	UDP_IP = str(socket.gethostname())
	TCP_IP = str(socket.gethostname())
	TCP_PORT = int(sys.argv[-1])

	aux = 3

elif sizeof > 2 and sys.argv[-2] == "-n":

	UDP_PORT = 58067
	UDP_IP = sys.argv[-1] + '.tecnico.ulisboa.pt'
	TCP_IP = sys.argv[-1] + '.tecnico.ulisboa.pt'
	TCP_PORT = 59000

	aux = 3

elif sizeof > 2 and sys.argv[-2] == "-e":
	
	UDP_PORT = int(sys.argv[-1])
	UDP_IP = str(socket.gethostname())
	TCP_IP = str(socket.gethostname())
	TCP_PORT = 59000

	aux = 3

elif (len(sys.argv) - aux) == 0:
	print "Invalid syntax. Please try again."
	sys.exit(0)

else:
	print "Invalid syntax. Please try again."
	sys.exit(0)


# UDP
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))



numeroPTCs = sizeof-aux

PTCs = []
ptcs = 'REG '
for i in range(0, numeroPTCs):
	PTCs.append(sys.argv[i+1])
	ptcs += str(sys.argv[i+1]) + ' '
ptcs += str(UDP_IP) + ' ' + str(TCP_PORT) +"\n"


sockUDP.sendto(ptcs, (UDP_IP, UDP_PORT))
data, addr = sockUDP.recvfrom(1024)
sockUDP.close()

print data 


signal.signal(signal.SIGINT, signal_handler)


s.listen(1)

while 1:
	conn, addr = s.accept()

	connection = list(addr)

	newWs = os.fork()
	if newWs == 0:
		data = conn.recv(BUFFER_SIZE)

		data_received = data.split()
		
		if data_received[1] not in PTCs:
			if(data_received[0] != 'WRQ' or len(data_received) < 5):
				MESSAGE = 'REP ERR\n'
			else:
			 MESSAGE = 'REP EOF\n'


		else:
			if data_received[1] == 'WCT':
				numberWords = len(data_received) - 4
				MESSAGE = "REP R " + data_received[3] + ' ' + str(numberWords) + '\n'
				print "WCT: " + data_received[2] + "\nNumber of words: " + str(numberWords) + "\n"

			elif data_received[1] == 'FLW':
				aux = len(data_received)
				longestWord =''
				size = 0
				for i in range(3, aux):
					if len(data_received[i]) > size:
						size = len(data_received[i])
						longestWord = data_received[i]
				MESSAGE = 'REP R ' + str(size) + " " + longestWord + '\n'
				print "FLW: " + data_received[2] + "\nLongest word: " + str(longestWord) + "\n"

			elif data_received[1] == 'UPP':
				aux = len(data_received)
				upperString =''
				for i in range(4, aux):
					upperString+= data_received[i].upper() + " "
				MESSAGE = 'REP F ' + data_received[3] + " " + upperString + '\n'
				print "UPP: " + str(data_received[2]) + "\nConvert to uppercase: " + str(upperString) + "\n"

			elif data_received[1] == 'LOW':
				aux = len(data_received)
				lowerString = ''
				for i in range(4, aux):
					lowerString += data_received[i].lower() + " "
				MESSAGE = 'REP F ' + data_received[3] + " " + lowerString + '\n'
				print "LOW: " + str(data_received[2]) + "\nConvert to lowercase: " + str(lowerString) + "\n"

			else:
				MESSAGE = 'REP ERR\n'


		conn.send(MESSAGE)

conn.close()
