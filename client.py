#Sending file
import socket, time
import glob
import os, sys
import threading

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

print("[CLIENT] CONNECTED\n")
#---------FUCNTIONS/SETUP--------
def send(msg):
    message = msg.encode('utf-8')
    client.send(message)

finished = False

def waiting(text):
    global finished

    print(f'{text}  ', end='', flush=True)
    while True:
        for frame in r'-\|/-\|/':
            # Back up one character then print our next frame in the animation
            print('\b', frame, sep='', end='', flush=True)

            time.sleep(0.2)

            if finished:
                print('\b', '#', sep='', end='', flush=True)
                print('')
                sys.exit()

def megaSend(conn, info):
    buf = 104900000 #100 Mebibytes, 104,900,000 bytes
    # print(f"Total length is {len(info)}")

    while True:
        if len(info) >= buf:
            conn.send(info[:buf]) 
            info = info[buf:]
        else:
            conn.send(info) #sending the rest
            break

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{round(num, 2)} {x}"
        num /= 1024.0

dir_path = os.path.dirname(os.path.realpath(__file__))
#------------------SEND FILE----------------------


for file in glob.glob(dir_path + '/send/*.*'):
    extension = file.split('.')[-1]
    name = file.split(dir_path)[-1].split('/send\\')[-1]

    finished = False
    thread = threading.Thread(target=waiting, args=('Reading file',))
    thread.start()

    myfile = open(file, 'rb')
    fileInfo = myfile.read()
    size = len(fileInfo)

    finished = True
    time.sleep(0.3)
    #-----------SEND FILE-----------
    send(f"INFO; .{size}.,{name},") #For server side parsing
    print(f'{name} {convert_bytes(size)}')
    
    finished = False
    thread = threading.Thread(target=waiting, args=('Sending file',))
    thread.start()

    megaSend(client, fileInfo)

    finished = True
    time.sleep(0.3)
    print('') #make newline for next file
    client.recv(1024) #Wait until "k" is sent by server
    time.sleep(0.5)

client.send('done'.encode('utf-8'))
input('All files sent, Press ENTER to close...')
