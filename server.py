#Recieving file
import socket
import os, sys

#-----------------------SERVER---------------------------
#CONSTANTS
IP = socket.gethostbyname(socket.gethostname())
PORT = 6437
ADDR = (IP, PORT)
#START SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print(f"[SERVER] Running on {socket.gethostname()} at {IP}:{PORT}")
#GET READY FOR CLIENT CONNECTION
server.listen()
conn, addr = server.accept()
print(f"[CONNECTION] {addr}")

#----------FUNCTIONS------------
def send(msg):
    message = msg.encode('utf-8')
    server.send(message)

dir_path = os.path.dirname(os.path.realpath(__file__))
#----------------RECIEVE FILE-------------------
while True:
    msg = conn.recv(1024).decode('utf-8')
    if msg.startswith('INFO'):
        size = msg.split('INFO; ')[-1].split('.')[1]
        name = msg.split('INFO; ')[-1].split(',')[1]
        fileInfo = conn.recv(int(size))
        f = open(f"{dir_path}/recieve/{name}", 'wb')
        f.write(fileInfo)
        f.close()
        print(f"RECIEVED FILE {name}")
        conn.send('k'.encode('utf-8'))
    elif msg == 'done':
        sys.exit()
