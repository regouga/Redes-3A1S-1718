#!/usr/bin/env python

import socket
import sys
import os

BUFFER_SIZE = 2048

sizeof = len(sys.argv)

if sizeof == 1:
	TCP_IP = str(socket.gethostname())
	TCP_PORT = 58067
elif (sizeof == 3) and (sys.argv[1] == "-n"):
	TCP_IP = sys.argv[2] + '.tecnico.ulisboa.pt'
	TCP_PORT = 58067
elif (sizeof == 3) and (sys.argv[1] == "-p"):
	TCP_IP = str(socket.gethostname())
	TCP_PORT = int(sys.argv[2])
elif sizeof == 5 and sys.argv[1] == '-n' and sys.argv[3] == '-p':
	TCP_IP = sys.argv[2] + '.tecnico.ulisboa.pt'
	TCP_PORT = int(sys.argv[4])
else:
	print "Invalid syntax. Please try again."
	sys.exit(0)


while(1):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))

	basicInput = raw_input('>')

	if len(basicInput) > 4:
		basicInput, PTC, filename = basicInput.split(" ")

	if basicInput == "list":

		s.sendall("LST\n")
		data = s.recv(BUFFER_SIZE)
		splitData = data.split()
		i = 1
		if (len(splitData) > 1):
			while (i <= int(splitData[1])):
				string = str(i) + '- ' + splitData[i+1] + ' - '
				if splitData[i+1] == "WCT":
					string += "word count"
				elif splitData[i+1] == "FLW":
					string += "find longest word"
				elif splitData[i+1] == "UPP":
					string += "convert text to upper case"
				elif splitData[i+1] == "LOW":
					string += "convert text to lower case"
				print string

				i += 1



	elif basicInput == "request":

		f = open(filename, "r")
		fileRead = f.read()
		statinfo = os.stat(filename)
		size = statinfo.st_size
		f.close()

		msg =  "REQ " + PTC + " "  + str(size) + " " + str(fileRead) + "\n"
		if PTC == "UPP" or PTC == "LOW":
			print str(size) + " Bytes to transmit"

		s.sendall(msg)
		i = size
		data = s.recv(BUFFER_SIZE)
		dataR = data.split()



		if len(dataR) < 4:
			if dataR[0] == "REP" and dataR[1] in ["R", "F"]:
				awnser = s.recv(BUFFER_SIZE)

				if dataR[1] == 'R':
					if PTC == 'WCT':
						print 'Number of words: ', awnser
					elif PTC == 'FLW':
						print 'File longest word: ', awnser

				elif dataR[1] == 'F':
					if PTC == "UPP":
						UPPfilename = os.path.splitext(filename)[0] + "_UPP.txt"
						fileUPP = open(UPPfilename, "w")
						fileUPP.write(awnser)
						sizeUPP = dataR[2]
						fileUPP.close()
						print "received file " + UPPfilename + "\n" + str(sizeUPP) + " Bytes"

					elif PTC == "LOW":
						LOWfilename = os.path.splitext(filename)[0] + "_LOW.txt"
						fileLOW = open(LOWfilename, "w")
						fileLOW.write(awnser)
						sizeLOW = dataR[2]
						fileLOW.close()
						print "received file " + LOWfilename + "\n" + str(sizeLOW) + " Bytes"
			else:
				print "Mensagem de erro" + str(data)

		else:
			awnser =''
			for ind in range(3, len(dataR)):
				awnser += dataR[ind] + " "
			if dataR[1] == 'R':
				if PTC == 'WCT':
					print 'Number of words:', awnser
				elif PTC == 'FLW':
					print 'File longest word:', awnser

			elif dataR[1] == 'F':
				if PTC == "UPP":
					UPPfilename = os.path.splitext(filename)[0] + "_UPP.txt"
					fileUPP = open(UPPfilename, "w")
					fileUPP.write(awnser)
					sizeUPP = dataR[2]
					fileUPP.close()
					print "received file " + UPPfilename + "\n" + str(sizeUPP) + " Bytes"

				elif PTC == "LOW":
					LOWfilename = os.path.splitext(filename)[0] + "_LOW.txt"
					fileLOW = open(LOWfilename, "w")
					fileLOW.write(awnser)
					sizeLOW = dataR[2]
					fileLOW.close()
					print "received file " + LOWfilename + "\n" + str(sizeLOW) + " Bytes"
		

	elif basicInput == "exit":
		s.close()
		sys.exit(0)

	else:
		print "Invalid syntax. Please try again."

	s.close()
