import socket
import threading
class Client(object):
    def __init__(self, addr, sock, number):
        self.sock = sock
        self.name = '<{}> (not logged in)'.format(addr)
        self.number = number
        self.lock = threading.Lock()
        # self.thread = threading.Thread(target=self.serve)
        # self.thread.start()
    def conect(self,host,port):
        self.sock.connect((host,port))
        # s = 'connection successfull'
        # s=bytes(s,'utf-8')
        # self.sock.sendall(s)
        print("connexion established")
        while True:
            # i=input("entrez le message !")
            # i=bytes(i, 'utf-8')
            # sock.sendall(i)
            data = sock.recv(1024)
            print(data)



        # while True:
        #     data = self.sock.recv(1024)
        #     # self.sock.close()
        # print(data)


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65433
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    arm = Client('127.0.0.1',sock,50)
    arm.conect(host,port)
