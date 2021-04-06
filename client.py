#Sending file
import socket, time
import glob
import os

PORT = 6437

#------------MAKE CONNECTION----------------------
while True:
    try:
        IP = input('Enter Server IP> ')
        ADDR = (IP, PORT)
        time.sleep(1)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        break
    except:
        print('IP Incorrect or client not ready to recieve...')

print("CONNECTED")
#---------FUCNTIONS/SETUP--------
def send(msg):
    message = msg.encode('utf-8')
    client.send(message)

dir_path = os.path.dirname(os.path.realpath(__file__))
#------------------SEND FILE----------------------


for file in glob.glob(dir_path + '/send/*.*'):
    extension = file.split('.')[-1]
    name = file.split(dir_path)[-1].split('/send\\')[-1]

    myfile = open(file, 'rb')
    fileInfo = myfile.read()
    size = len(fileInfo)

    #-----------SEND FILE-----------
    print(f"EXNTENSION ---> {extension}, NAME ---> {name}, SIZE ---> {size}")
    send(f"INFO; .{size}.,{name},") #For server side parsing

    time.sleep(.2)
    client.sendall(fileInfo)
    print(f"SENT FILE\n\n")
    time.sleep(0.5)
input('\n\n\n\nPress Enter to close...')
