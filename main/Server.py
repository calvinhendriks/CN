from threading import Thread
import threading
import math
import time
import queue
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from datetime import datetime
from scipy.stats import truncnorm

class Server(Thread):
    def __init__(self, chunksize, ackq, clientq, serverq, mode, scheme, rtt, load, ackdelay = 1, bandwith = 54):
        super(Server,self).__init__()
        # print("Server: initiliazed")
        self.filesize = 100
        self.chunksize = chunksize
        self.ackq = ackq
        self.clientq = clientq
        self.serverq = serverq
        self.mode = mode
        self.scheme = scheme
        self.rtt = rtt
        self.load = load
        self.ackdelay = ackdelay
        self.bandwith = bandwith
        self._stopevent = threading.Event(  )


        self.totaldelay = 0


        if self.mode == "send":
            for i in range(math.ceil(self.filesize/self.chunksize)):
                serverq.put(i)


    def sendfiles(self):
        print("server: sendfiles() called")

    def receivefiles(self):
        # print("Server: receiving files...")
        # ("Server: " + self.scheme + " scheme")
        receivedchunks = 0
        waitingacks = 0
        receivedtimes = []
        timedif = datetime.now() - datetime.now()
        while not self._stopevent.isSet():
            if self.scheme == "sequential":
                if not self.serverq.empty():
                    chunk = self.serverq.get()
                    # print(self.getName() + ": received " + str(chunk))
                    receivedchunks += 1
                    # print(receivedchunks)
                    ack = "ack"
                    # print(self.getName() + ": send " + ack)
                    self.ackq.put(ack)
                    self.totaldelay += self.load
                    self.totaldelay += self.rtt[receivedchunks]
                    self.totaldelay += (self.chunksize * 8 / self.bandwith) * 1000
            #delayed scheme
            else:
                if not self.serverq.empty():
                    receivedchunks += 1
                    waitingacks += 1
                    chunk = self.serverq.get()
                    # print(self.getName() + ": received " + str(chunk))
                    receivedtimes.append(datetime.now())

                    if(receivedchunks % self.ackdelay == 0):
                        ack = "ack"
                        # print(self.getName() + ": send " + ack)
                        self.ackq.put(ack)
                        waitingacks = 0
                        self.totaldelay += self.load
                        self.totaldelay += self.rtt[receivedchunks]
                        self.totaldelay += ((self.chunksize * 8 / self.bandwith) * 2) * 1000
                        self.totaldelay += (self.rtt[receivedchunks + 1] / 2)

                elif(waitingacks >= 1):
                    timedif = datetime.now() - receivedtimes[receivedchunks-1]
                    # print(int(timedif.total_seconds() * 1000))
                    if(int(timedif.total_seconds() * 1000) > 100):
                        ack = "ack"
                        print(self.getName() + ": timeout expired!")
                        # print(self.getName() + ": send " + ack)
                        waitingacks = 0
                        self.ackq.put(ack)
                        self.totaldelay += 0 #timeout value
                        self.totaldelay += self.load
                        self.totaldelay += (self.chunksize * 8 / self.bandwith) * 1000
                        self.totaldelay += self.rtt[receivedchunks]


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