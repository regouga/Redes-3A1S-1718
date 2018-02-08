#!/usr/bin/env python

import socket
import sys
import os

BUFFER_SIZE = 1024
 # WCT FLW UPP LOW



def slice_list(input, size):
	input_size = len(input)
	slice_size = input_size / size
	remain = input_size % size
	result = []
	iterator = iter(input)
	for i in range(size):
		result.append([])
		for j in range(slice_size):
			result[i].append(iterator.next())
		if remain:
			result[i].append(iterator.next())
			remain -= 1
	return result

def child(filename, recvPTC):
	data = ""
	stringToSend = ""
	PTCip = []
	PTCport = []
	wsPTCS = [0, 0, 0, 0]
	f2 = open("file_processing_tasks.txt", 'r')
	lines = f2.readlines()
	for line in lines:
		splitedLine = line.split()
		if str(splitedLine[0]) == "WCT":
			wsPTCS[0] += 1
		elif str(splitedLine[0]) == "FLW":
			wsPTCS[1] += 1
		elif str(splitedLine[0]) == "UPP":
			wsPTCS[2] += 1
		elif str(splitedLine[0]) == "LOW":
			wsPTCS[3] += 1
	f2.close()

	newpath = r'input_files'
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	openingFilename = "/input_files/" + filename
	fileUser = open(os.path.join(newpath, filename), 'r')
	linesUser = fileUser.readlines()
	numberLines = len(linesUser)

	print filename, 

	if recvPTC == "WCT":
		wsptc = wsPTCS[0]
		index = 0

	elif recvPTC == "FLW":
		wsptc = wsPTCS[1]
		index = 1

	elif recvPTC == "UPP":
		wsptc = wsPTCS[2]
		index = 2

	elif recvPTC == "LOW":
		wsptc = wsPTCS[3]
		index = 3


	if wsptc == 0:
		print "There's no available working servers to process such PTC."
	else:

		f3 = open("file_processing_tasks.txt", 'r')
		for line in lines:
			splitedLine2 = line.split()
			if splitedLine2[0] == recvPTC:
				PTCport.append(int(splitedLine2[2]))
				PTCip.append(splitedLine2[1])



		linesPerFile = numberLines // wsptc
		splitedFile = slice_list(linesUser, wsptc)

		fileNameArrray = filename.split(".")
		fileNameWithoutExtention = str(fileNameArrray[0])
		numPart = 0


		aux = 0
		WCTint = 0
		totalSize = 0
		stringL = ""
		stringToSend = ""
		stringToPrint = recvPTC + ": "

		for listToWS in splitedFile:
			data = ''
			numPartCheio = str(numPart).zfill(3)
			newFileName = fileNameWithoutExtention + str(numPartCheio) + ".txt"
			fileWrite = open(os.path.join(newpath, newFileName), 'a')

			for linha in listToWS:
				fileWrite.write(linha)
				data += linha + ' '
			numPart += 1


			fileWrite.close()
			size = os.path.getsize(os.path.join(newpath, newFileName))
			if aux < wsptc:

				tosendip = PTCip[aux]
				tosendport = PTCport[aux]

				stringToPrint += tosendip + " " + str(tosendport) + "\n"

				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((tosendip, tosendport))

				MESSAGE = "WRQ " + recvPTC + ' ' + newFileName + ' ' +  str(size) + ' ' + data

				s.send(MESSAGE)
				data = s.recv(BUFFER_SIZE)

				s.close()

				dataS = data.split()

				if index == 0:
					#WCT
					WCTint += int(dataS[3])

				elif index == 1:
					if len(dataS[3]) > totalSize:
						totalSize = len(dataS[3])
						stringL = str(dataS[3])

				elif index == 2 or index == 3:
					for i in range(3, len(dataS)):
						stringL += dataS[i] + " "
					totalSize += int(dataS[2])
				aux += 1
		print stringToPrint

		if index == 0:
			stringToSend = "REP R " + str(len(str(WCTint))) + " " + str(WCTint)

		elif index == 1:
			stringToSend = "REP R " + str(totalSize) + " " + stringL

		elif index == 2 or index == 3:
			stringToSend = "REP F " + str(totalSize) + " " + stringL

	return stringToSend


def registerUDP():

	sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sockUDP.bind((IP, PORT))
	numberWS = 0

	while True:
		dataUDP, addr = sockUDP.recvfrom(1024)
		dataUDParray = dataUDP.split()
		availablePTCs = ['WTC', 'FLW', 'UPP', 'LOW']
		lenUDP = len(dataUDParray)

		if dataUDParray[0] == "REG":
			if lenUDP == 1 or lenUDP > 7:
				msg = 'RAK ERR'

			elif numberWS < 10:

				msg = 'RAK OK'
				Faux = open('file_aux.txt', 'a')
				msgFile = "free 0 " + dataUDParray[-2] + ' ' + dataUDParray[-1]
				Faux.write(msgFile)
				Faux.close()
				dataWS = "+"
				for i in range(1, len(dataUDParray)):
					dataWS += dataUDParray[i] + " "

				f2 = open("file_processing_tasks.txt", 'a')
				fpt = ""
				for j in range (1, len(dataUDParray)-2):
					fpt = dataUDParray[j] + " " + dataUDParray[-2] + " " + dataUDParray [-1] + "\n"
					f2.write(fpt)
					fpt = ""

				numberWS += 1
				print dataWS
				f2.write(fpt)
				f2.close()

			else:
				for i in range(0, lenUDP -2):
					if dataUDParray[i+1] not in availablePTCs:
						msg = 'RAK ERR'

			sockUDP.sendto(msg, addr)

				

		elif dataUDParray[0] == "UNR":
			f2 = open("file_processing_tasks.txt", 'r')
			lines = f2.readlines()
			f2.close()

			IP1 = str(dataUDParray[1])
			PORT1 = int(dataUDParray[2])

			closingMessage = "-"

			flag = 0
			f3 = open("file_processing_tasks.txt", 'w')
			for line in lines:
				splitedLine = line.split()
				IP2 = str(splitedLine[1])
				PORT2 = int(splitedLine[2])
				if IP1 != IP2 or PORT1 != PORT2:
					f3.write(line)
				else:
					closingMessage += str(splitedLine[0]) + " "
					flag = 1
			f3.close()
			if (flag == 1):
				closingMessage += str(IP1) + " " + str(PORT1)
				print closingMessage


def waitingTCP():

	sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockTCP.bind((IP, PORT))
	sockTCP.listen(1)
	data1 = ""

	while True:
		conn, addr = sockTCP.accept()
		data = conn.recv(BUFFER_SIZE)
		num = 0

		aux = data.split("\n")


		analise = aux[0].split(" ")


		lista = ""
		for i in range(3, len(analise)):
			lista += analise[i] + " "

		aux[0] = lista

		if analise[0] == 'LST':
			print "List request: " + str(IP) + str(PORT)
			listPTCs = []
			fileReading = open("file_processing_tasks.txt", 'r')
			lines = fileReading.readlines()
			for line in lines:
				splitedLine = line.split()

				if "WCT" in splitedLine:
					if "WCT" not in listPTCs:
						listPTCs.append("WCT")
				if "FLW" in splitedLine:
					if "FLW" not in listPTCs:
						listPTCs.append("FLW")

				if "UPP" in splitedLine:
					if "UPP" not in listPTCs:
						listPTCs.append("UPP")

				if "LOW" in splitedLine:
					if "LOW" not in listPTCs:
						listPTCs.append("LOW")

			number = len(listPTCs)
			strtoprint = ""
			if number == 0:
				data1 = "FPT EOF"
			else:
				data1 = "FPT " + str(number) + " "
				for p in listPTCs:
					data1 += p + " "
					strtoprint += p + " "
			conn.send(data1)
				



		elif analise[0] == "REQ":
			ptc = str(analise[1])

			newpath = r'input_files'
			if not os.path.exists(newpath):
				os.makedirs(newpath)

			numCheio = str(num)
			numCheio2 = numCheio.zfill(5)
			name = str(numCheio2) + ".txt"
			f = open(os.path.join(newpath, name), 'w')
			for h in range(0, len(aux)):
				if h == len(aux)-1:
					toWrite = aux[h]
				else:
					toWrite = aux[h] + "\n"
				f.write(toWrite)
			f.close()

			newpid = os.fork()
			if newpid == 0:
				data1 = child(name, ptc)
				conn.send(data1)
			num+= 1


		  # echo
	conn.close()


#-------------------------------------------------------------------------------

sizeof = len(sys.argv)

if sizeof == 1:
	IP = str(socket.gethostname())
	PORT = 58067
elif (sizeof == 3) and (sys.argv[1] == "-p"):
	IP = str(socket.gethostname())
	PORT = int(sys.argv[2])

open("file_processing_tasks.txt", 'w').close()
open("file_aux.txt", 'w').close()

UDPson = os.fork()
if UDPson == 0:
	registerUDP();
else:
	waitingTCP();

while True:
	continue
