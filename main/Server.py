from threading import Thread
import threading
import math
import time
import queue
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class Server(Thread):
    def __init__(self, chunksize, ackq, clientq, serverq, mode,scheme, mu, sigma, load, ackdelay = 1):
        super(Server,self).__init__()
        print("server init")
        self.filesize = 100
        self.chunksize = chunksize
        self.ackq = ackq
        self.clientq = clientq
        self.serverq = serverq
        self.mode = mode
        self.scheme = scheme
        self.mu = mu
        self.sigma = sigma
        self.load = load
        self.ackdelay = ackdelay
        self._stopevent = threading.Event(  )
        self.rtt = np.random.normal(mu, sigma, 100)
        #print(self.rtt)
        self.totaldelay = 0
        print(datetime.now())
        if self.mode == "send":
            for i in range(math.ceil(self.filesize/self.chunksize)):
                serverq.put(i)


    def sendfiles(self):
        print("server: sendfiles() called")

    def receivefiles(self):
        print("Server: receiving files...")
        print("Server: " + self.scheme + " scheme")
        receivedchunks = 0
        receivetime = 0
        while not self._stopevent.isSet():
            if self.scheme == "sequential":
                if not self.serverq.empty():
                    chunk = self.serverq.get()
                    print(self.getName() + ": received " + str(chunk))
                    receivedchunks += 1
                    #print(receivedchunks)
                    ack = "ack"
                    print(self.getName() + ": send " + ack)
                    self.ackq.put(ack)
                    self.totaldelay += self.load
                    self.totaldelay += self.rtt[receivedchunks]
            #delayed scheme
            else:
                if not self.serverq.empty():
                    chunk = self.serverq.get()
                    print(self.getName() + ": received " + str(chunk))
                    receivedchunks += 1
                    receivetime = datetime.now()
                    timedif = datetime.now() - receivetime
                    if(receivedchunks % self.ackdelay == 0):
                        ack = "ack"
                        print(self.getName() + ": send " + ack)
                        self.ackq.put(ack)
                        self.totaldelay += self.load
                        self.totaldelay += self.rtt[receivedchunks]
                        self.totaldelay += (self.rtt[receivedchunks + 1] / 2)
                    elif(int(timedif.total_seconds() * 1000) > 100):
                        ack = "ack"
                        print(self.getName() + ": send " + ack)
                        self.ackq.put(ack)
                        self.totaldelay += self.load
                        self.totaldelay += self.rtt[receivedchunks]


                    #print(receivedchunks)



        return



    def run(self):
        if self.mode == "send":
            self.sendfiles()
        if self.mode == "receive":
            self.receivefiles()


    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        Thread.join(self, timeout)

    def get_delay(self):
        return self.totaldelay