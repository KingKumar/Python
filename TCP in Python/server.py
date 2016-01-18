# Server program, run on BETA
# 1. ON BETA: python server.py 5000 10001
# 2. ON BETA: troll -C 164.107.112.68 -S 164.107.112.70 -a 5000 -b 6000 10001 -r -t -x 0
# 3. ON GAMMA: troll -C 164.107.112.70 -S 164.107.112.68 -a 6000 -b 5000 10001 -r -t -x 0
# 4. ON GAMMA: python client.py 164.107.112.68 5000 10001 11.jpg
import socket
import sys
import os
import struct
import select

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = sys.argv[1]              # Server port
SERVERIP = "164.107.112.68" #IP address for gamma
TROLLPORT = sys.argv[2] # Troll port
TROLLPORT = int(TROLLPORT,10)
INTPORT = int(PORT, 10)
a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a.bind((HOST, INTPORT))
print "Waiting for packets..."
receivedOne = 0
receivedTwo = 0
receivedThree = 0
flag = 0

seg1 = struct.Struct('!4sIII4s')
seg2 = struct.Struct('!4sIII20s')
seg3 = struct.Struct('!4sIII992s')

data = 1
while data:
	data = None
	while not data:
		data, addr = a.recvfrom(1000)
	print 'data from ', addr, '-> ', data
	if receivedOne == 0:
		data = seg1.unpack(data)
	if receivedOne != 0 & receivedTwo == 0:
		data = seg2.unpack(data)
	if receivedOne != 0 & receivedTwo != 0 & receivedThree == 0:
		data = seg3.unpack(data)
	print 'unpacked data-> ', data
	flag = int(str(data[2]).strip())
	print 'flag value ', flag
	print 'flag value ', flag
	print 'flag value ', flag
   	if flag == 1 & receivedOne == 0:
	    print 'Received segment 1 from ', addr
	    receivedOne = 1
	    data = data[4]
	    filesize = data
	    print 'Filesize: ', filesize
	    ACK = struct.pack('B', 1)
	    a.sendto(ACK, (SERVERIP, TROLLPORT))
   	if flag == 2 & receivedTwo == 0:
   		print 'Received segment 2 from ', addr
   		print 'Seg2 data ', data
   		data = seg2.unpack(data)
   		receivedTwo = 2
   		data = data[4]
   		filename = data.decode()
   		print 'Filename: ', filename
   		ACK = struct.pack('B', 0)
   		a.sendto(ACK, (SERVERIP, TROLLPORT))
   	if flag == 3 & receivedOne != 0 & receivedTwo != 0:
   		if receivedThree == 0:
   			if not os.path.exists('newDirectory'):
   				os.makedirs('newDirectory')
			os.chdir('newDirectory')
			file = open('directory', 'w+')
			receivedThree = 1
   		print 'Received segment 3 from ', addr
   		data = data[4]
   		print 'Received ->', data   
   		file.write(data)
	else:
   		# Timeout
		print 'Timeout.'