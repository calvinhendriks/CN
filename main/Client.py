from threading import Thread
import threading
import time
import math
import queue




class Client(Thread):
    def __init__(self, chunksize, ackq, clientq, serverq, mode,scheme, ackdelay = 1):
        super(Client,self).__init__()
        print("Client: initialized")
        self.filesize = 100
        self.chunksize = chunksize
        self.ackq = ackq
        self.clientq = clientq
        self.serverq = serverq
        self.mode = mode
        self.scheme = scheme
        self.ackdelay = ackdelay
        if self.mode == "send":
            for i in range(math.ceil(self.filesize/self.chunksize)):
                #print(i)
                self.clientq.put(i)



    def sendfiles(self):
        #sequential scheme
        if self.scheme == "sequential":
            print("Client: sending files...")
            print("Client: " + self.scheme + " scheme")
            chunk = self.clientq.get()
            print(self.getName() + ": send " + str(chunk))
            self.serverq.put(chunk)
            while True:
                #if prevrious chunks were acknowledged
                if not self.ackq.empty():
                    ack = self.ackq.get()
                    print(self.getName() + ": received " + ack)
                    if not self.clientq.empty():
                        chunk = self.clientq.get()
                        print(self.getName() + ": send " + str(chunk))
                        self.serverq.put(chunk)
                    #clientqueue is empty
                    else:
                        print("Client: queue empty!")
                        return
        #delayed scheme
        else:
            print("Client: Sending files")
            print("Client: " + self.scheme + " scheme")
            for i in range(self.ackdelay):
                chunk = self.clientq.get()
                print(self.getName() + " send " + str(chunk))
                self.serverq.put(chunk)
            while True:
                if not self.ackq.empty():
                    ack = self.ackq.get()
                    print(self.getName() + ": received " + ack)
                    if self.clientq.qsize() >= self.ackdelay:
                        for i in range(self.ackdelay):
                            chunk = self.clientq.get()
                            print(self.getName() + " send " + str(chunk))
                            self.serverq.put(chunk)
                    else:
                        if not self.clientq.empty():
                            for i in range(self.clientq.qsize()):
                                chunk = self.clientq.get()
                                print(self.getName() + " send " + str(chunk))
                                self.serverq.put(chunk)
                        else:
                            print("Client: queue empty!")
                            return



    def receivefiles(self):
        print("")


    def run(self):
        if self.mode == "send":
            self.sendfiles()
        if self.mode == "receive":
            self.receivefiles()