import socket
import os
from _thread import *
from time import sleep
from multiprocessing import Process
import sys
from threading import Thread

class server:
    peer_dict={}
    peer_availability={}
    def __init__(self):
        pass

    def multi_threaded_client(self,connection,address):
        connection.send(str.encode('Server is working:'))
        while True:
            try:
                data = connection.recv(2048)
                response = 'Server message: ' + data.decode('utf-8')
                if not data:
                    break
                connection.sendall(str.encode(response))
            except:
                print("connection closed")
        connection.close()
        self.peer_dict.pop(address)
        self.peer_availability.pop(address)
        print("gone")
        print(self.peer_dict)


    def accept_peer(self):
        ServerSideSocket = socket.socket()
        host = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
        print(host)
        port = 2006
        thread_count = 0
        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        ServerSideSocket.listen(5)
        while True:
            Client, address = ServerSideSocket.accept()
            Client.sendall(b"Approved")
            data = Client.recv(2048)
            data=data.decode('utf-8')
            self.peer_dict[address]=data
            self.peer_availability[address]=1
            print(self.peer_dict)
            print(self.peer_availability)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(server.multi_threaded_client, (self, Client, address))
            thread_count += 1
            print('Thread Number: ' + str(thread_count))
            # break
        ServerSideSocket.close()
    
#     def peer_work_distributer():
#         pass
    def starter():
        server.accept_peer()
        # accept_peer = Thread(target=server.accept_peer, daemon=True, name='peer tracker')
        # accept_peer.start()
        # # wasss = Thread(target=server.peer_work_distributer, daemon=True, name='distribute work')
        # # wasss.start()

        # accept_peer.join()
# wasss.join()
s= server()
s.accept_peer()

# server.start()