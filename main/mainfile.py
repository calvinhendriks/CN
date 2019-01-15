from main.Server import Server
from main.Client import Client
import numpy as np
import scipy.stats as stats
from threading import Thread
import queue
import sys


if __name__ =='__main__':
    #modes: upload / download
    #schemes: sequential, delayed

    #ARGUMENTS
    repetitions = 5
    chunksizes = [1,4,5,8]
    means = [10, 50, 100, 150]
    stddevs = [8.8, 44, 88, 132]
    serverload = [10,100,300]

    #RESULT ARRAYS
    # Use a compound data type for structured arrays
    dt = np.dtype([('scheme', np.unicode_, 16), ('size', np.int32), ('value', np.float64, (repetitions,))])

    chunkresult = np.array([('seq', 1 , np.zeros(repetitions)),('seq', 4 , np.zeros(repetitions)),
                     ('seq', 5 , np.zeros(repetitions)),('seq', 8 , np.zeros(repetitions)),
                     ('del', 1 , np.zeros(repetitions)),('del', 4 , np.zeros(repetitions)),
                     ('del', 5 , np.zeros(repetitions)) ,('del', 8 , np.zeros(repetitions))  ], dtype=dt)

    #Other
    rtt100 = []
    for i in range(1000):
        rtt100.append(100)

    lower, upper = 1, 1000
    mu, sigma = 12, 10.56
    X = stats.truncnorm(
        (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    # N = stats.norm(loc=mu, scale=sigma)
    rtt = X.rvs(size=100)




    for x in range(repetitions):
        clientq = queue.Queue()
        serverq = queue.Queue()
        ackq = queue.Queue()
        print(x)

        #+++++++++++++++++++++Chunks++++++++++++++++++++++++++++++++++++++++++

        for y in range(len(chunksizes)):

            #++++++++++++++++++++++Sequential++++++++++++++++++++++++++++++

            s = Server(chunksizes[y], ackq, clientq, serverq, "receive" , "sequential" , rtt100, 10)
            c = Client(chunksizes[y], ackq, clientq, serverq, "send", "sequential")

            s.setName("Server")
            c.setName("Client")
            s.start()
            c.start()
            c.join()

            while True:
                if not c.is_alive():
                    delay = s.get_delay()
                    if(chunksizes[y] == 1):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 1)] = delay
                    elif(chunksizes[y] == 4):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 4)] = delay
                    if(chunksizes[y] == 5):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 5)] = delay
                    elif(chunksizes[y] == 8):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 8)] = delay
                    s.join()

                    break
                    #sys.exit()

            #++++++++++++++++++++++Delayed++++++++++++++++++++++++++++++


            s = Server(4, ackq, clientq, serverq, "receive" , "delayed" , rtt100, 10, 2)
            c = Client(4, ackq, clientq, serverq, "send", "delayed", 2)

            s.setName("Server")
            c.setName("Client")
            s.start()
            c.start()
            c.join()

            while True:
                if not c.is_alive():
                    delay = s.get_delay()
                    if(chunksizes[y] == 1):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'del', chunkresult['size'] == 1)] = delay
                    elif(chunksizes[y] == 4):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'del', chunkresult['size'] == 4)] = delay
                    if(chunksizes[y] == 5):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'del', chunkresult['size'] == 5)] = delay
                    elif(chunksizes[y] == 8):
                        chunkresult['value'][:,x][np.logical_and(chunkresult['scheme'] == 'del', chunkresult['size'] == 8)] = delay
                    s.join()

                    break

        # #+++++++++++++++++++++RTT++++++++++++++++++++++++++++++++++++++++++
        #
        # for y in range(means):
        #
        #     #++++++++++++++++++++++Sequential++++++++++++++++++++++++++++++
        #
        #     s = Server(1, ackq, clientq, serverq, "receive" , "sequential" , 100, 20,50)
        #     c = Client(1, ackq, clientq, serverq, "send", "sequential")
        #
        #     s.setName("Server")
        #     c.setName("Client")
        #     s.start()
        #     c.start()
        #     c.join()
        #
        #     while True:
        #         if not c.is_alive():
        #             delay = s.get_delay()
        #             chunkresult = np.append(chunk,delay)
        #             print(delay)
        #             s.join()
        #             break
        #             #sys.exit()
        #
        #     #++++++++++++++++++++++Delayed++++++++++++++++++++++++++++++
        #
        #
        #     s = Server(4, ackq, clientq, serverq, "receive" , "delayed" , 100, 20,50,2)
        #     c = Client(4, ackq, clientq, serverq, "send", "delayed", 2)
        #
        #     s.setName("Server")
        #     c.setName("Client")
        #     s.start()
        #     c.start()
        #     c.join()
        #
        #     while True:
        #         if not c.is_alive():
        #             delay = s.get_delay()
        #             print(delay)
        #             s.join()
        #             break

    chunk1 = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 1)]
    print(chunk1)

    chunk4 = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 4)]
    print(chunk4)

    chunk5 = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 5)]
    print(chunk5)

    chunk8 = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['size'] == 8)]
    print(chunk8)