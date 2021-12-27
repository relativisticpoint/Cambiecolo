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

    def send(self, msg):
        with self.lock:
            self.sock.send(msg)

    def run(self):
        for line in self.sock.makefile():
            args = line.rstrip().split()
            cmd = args.pop().upper()
            method = getattr(self, 'do_{}'.format(cmd), None)
            if method is None:
                self.write('ERROR unknown command {}\n'.format(cmd))
            else:
                try:
                    method(*args)
                except Exception as e:
                    self.send('ERROR in {}: {}\n'.format(cmd, e))
                else:
                    self.send('OK\n')
    def conect(self,host,port):
        self.sock.connect((host,port))
        while True:
            # s = 'connection successfull'
            # s=bytes(s,'utf-8')
            # self.sock.sendall(s)
            data = self.sock.recv(1024)
            # self.sock.close()
            print(data)







if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65432
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    arm = Client('127.0.0.2',sock,50)
    arm.conect(host,port)