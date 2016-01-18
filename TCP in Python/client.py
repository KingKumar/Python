# Client program, run on GAMMA
# 1. ON BETA: python server.py 5000 10001
# 2. ON BETA: troll -C 164.107.112.68 -S 164.107.112.70 -a 5000 -b 6000 10001 -r -t -x 0
# 3. ON GAMMA: troll -C 164.107.112.70 -S 164.107.112.68 -a 6000 -b 5000 10001 -r -t -x 0
# 4. ON GAMMA: python client.py 164.107.112.68 5000 10001 11.jpg
import socket
import sys
import os
import struct
import select
import time

HOST = sys.argv[1]    # The remote host
PORT = sys.argv[2]    # The remote port encoded
PORT = int(PORT, 10)
TROLLPORT = sys.argv[3] # Troll port
TROLLPORT = int(TROLLPORT,10)
file = open(sys.argv[4], "rb")
CLIENTIP = "164.107.112.70" #IP address for gamma
FLAGONE = 1
FLAGTWO = 2
FLAGTHREE = 3
ACK = 0
BYTEHOST = socket.inet_aton(HOST)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((CLIENTIP, 6000))

filesize = str(os.path.getsize(sys.argv[4])).encode()
filename = sys.argv[4].encode()

seg1 = struct.Struct('!4sIII4s')


#First segment
segone = seg1.pack(BYTEHOST, PORT, FLAGONE, ACK, filesize)
while ACK == 0:
	print 'Sending segment'
	s.sendto(segone, (CLIENTIP, TROLLPORT))
	ACKin, addr = s.recvfrom(1)
	ACK = struct.unpack('B', ACKin)
	sleep(.05)
print 'Received ACK', ACK, '  from ', addr

seg2 = struct.Struct('!4sIII20s')

#Second segment
ACK = 1
segtwo = seg2.pack(BYTEHOST, PORT, FLAGTWO, ACK, filename)
while ACK == 1:
	print 'Sending next segment'
	s.sendto(segtwo, (CLIENTIP, TROLLPORT))
	ACKin, addr = s.recvfrom(1)
	ACK = struct.unpack('B', ACKin)
	sleep(.05)
print 'Received ACK', ACK, '  from ', addr


seg3 = struct.Struct('!4sIII992s')

#Third segment(s)
byte = file.read(992)
while (byte):
	ACK = struct.unpack('B', ACKin)
	segthree = seg3.pack(BYTEHOST, PORT, FLAGTHREE, ACK, byte)
	ACK = struct.pack('B', ACK)
	while ACK == 0:
		print 'Sending next segment'
		s.sendto(segthree, (CLIENTIP, TROLLPORT))
		ACKin, addr = s.recvfrom(1)
		print 'Received ACK', ACKin, ' from ', addr
		sleep(.05)
	while ACK == 1:
		print 'Sending next segment'
		s.sendto(segthree, (CLIENTIP, TROLLPORT))
		ACKin, addr = s.recvfrom(1)
		print 'Received ACK', ACKin, '  from ', addr
		sleep(.05)
	byte = file.read(992)

s.close()
