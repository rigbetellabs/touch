#----- A simple TCP client program in Python using send() function -----

import socket
import pyautogui

sw,sh = pyautogui.size()
print(sw, sh)

while(True):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    clientSocket.connect(("192.168.1.157",9090))

    dataFromServer = clientSocket.recv(1024)

    data = dataFromServer.decode()
    if data :
        new_point = data[1:-1] 
        new_data = tuple(map(float, new_point.split(',')))
        #print(new_data)

        pyautogui.moveTo(new_data[0]*sw, new_data[1]*sh)
        #pyautogui.click(new_data[0]*sw, new_data[1]*sh)
        
    
        
    

    


