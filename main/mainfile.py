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

    s = Server(4, ackq, clientq, serverq, "receive" , "sequential" , 100, 20,50)
    c = Client(4, ackq, clientq, serverq, "send", "sequential")

    s.setName("Server")
    c.setName("Client")
    s.start()
    c.start()
    c.join()

    while True:
        if not c.is_alive():
            delay = s.get_delay()
            print(delay)
            s.join()
            break
            #sys.exit()

    s = Server(4, ackq, clientq, serverq, "receive" , "delayed" , 100, 20,50,2)
    c = Client(4, ackq, clientq, serverq, "send", "delayed", 2)

    s.setName("Server")
    c.setName("Client")
    s.start()
    c.start()
    c.join()

    while True:
        if not c.is_alive():
            delay = s.get_delay()
            print(delay)
            s.join()
            break

