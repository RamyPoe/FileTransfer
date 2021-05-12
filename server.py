#Recieving file
import socket
import os, sys
import threading
import time

#-----------------------SERVER---------------------------
#CONSTANTS
IP = socket.gethostbyname(socket.gethostname())
PORT = 6437
ADDR = (IP, PORT)

finished = False
#START SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print(f"[SERVER] Running on {socket.gethostname()} at {IP}:{PORT}")
#GET READY FOR CLIENT CONNECTION
server.listen()
conn, addr = server.accept()
print(f"[CONNECTION] {addr}\n")

#----------FUNCTIONS------------
def progress_bar(total, progress):
    """
    Displays or updates a console progress bar.
    """
    status = "Receiving..."
    soFar = progress
    barLength = 40
    progress = float(progress) / float(total)
    if progress >= 1.:
        # progress, status = 1, "\r\n"
        progress, status = 1, "Received!"

    block = int(round(barLength * progress))
    text = "\r{} [{}] {:.0f}% {}/{}{}".format(status, "#" * block + "-" * (barLength - block), round(progress * 100, 0), convert_bytes(soFar), convert_bytes(total), ' '*8) #Last one creates empy space so as to completly overwrite the last progression
    sys.stdout.write(text)
    sys.stdout.flush()

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

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{round(num, 2)} {x}"
        num /= 1024.0

def recvall(conn, length):
    """ Retreive all info in buffer system """
    atOnce = 104900000 #100 Mebibytes
    total = int(length)
    length = int(length)
    buf = b''
    while length > 0:
        data = conn.recv(atOnce)
        if not data:
            return data
        buf += data
        length -= len(data)
        # print(f'{len(buf)}/{total}')
        progress_bar(total, len(buf))
    
    print('')
    return buf

dir_path = os.path.dirname(os.path.realpath(__file__))
#----------------RECIEVE FILE-------------------
while True:
    msg = conn.recv(1024).decode('utf-8')
    if msg.startswith('INFO'):
        size = msg.split('INFO; ')[-1].split('.')[1]
        name = msg.split('INFO; ')[-1].split(',')[1]
        print(f"{name} {convert_bytes(int(size))}")

        fileInfo = recvall(conn, size)
        #Spinning animation while writing to the file
        finished = False
        thread = threading.Thread(target=waiting, args=('Writing to file',))
        thread.start()

        f = open(f"{dir_path}/recieve/{name}", 'wb')
        f.write(fileInfo)
        f.close()
        #Show that writing to the file has finished (stop animation)
        finished = True
        time.sleep(0.3)

        print('')
        conn.send('k'.encode('utf-8')) #Tell that ready to receive next file
    elif msg == 'done':
        break

input("\nAll files have been received, press ENTER to close...")
