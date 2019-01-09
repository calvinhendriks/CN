from main.Server import Server
from main.Client import Client
from threading import Thread
import queue
import sys


if __name__ =='__main__':
    #modes: upload / download
    #schemes: sequential, delayed
    clientq = queue.Queue()
    serverq = queue.Queue()
    ackq = queue.Queue()



    s = Server(4, ackq, clientq, serverq, "receive" , "sequential" )
    c = Client(4, ackq, clientq, serverq, "send", "sequential")
    s.setName("Server")
    c.setName("Client")
    s.start()
    print("debug")
    c.start()
    c.join()

    while True:
        if not c.is_alive():
            s.join()
            sys.exit()

