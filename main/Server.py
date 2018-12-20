from threading import Thread
import threading
import math
import time
import queue

class Server(Thread):
    def __init__(self, chunksize, ackq, clientq, serverq, mode,scheme):
        super(Server,self).__init__()
        print("server init")
        self.filesize = 100
        self.chunksize = chunksize
        self.ackq = ackq
        self.clientq = clientq
        self.serverq = serverq
        self.mode = mode
        self.scheme = scheme
        self._stopevent = threading.Event(  )
        if self.mode == "send":
            for i in range(math.ceil(self.filesize/self.chunksize)):
                serverq.put(i)

    def sendfiles(self):
        print("server: sendfiles() called")

    def receivefiles(self):
        print("Server: receiving files...")
        while not self._stopevent.isSet():
            if self.scheme == "sequential":
                if not self.serverq.empty():
                    chunk = self.serverq.get()
                    print(self.getName() + " received " + str(chunk))
                    ack = "ack"
                    print(self.getName() + " send " + ack)
                    self.ackq.put(ack)
            else:
                print(self.scheme)
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
