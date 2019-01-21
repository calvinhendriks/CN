from main.Server import Server
from main.Client import Client
import numpy as np
import scipy.stats as stats
from threading import Thread
import queue
import sys
import matplotlib.pyplot as plt


if __name__ =='__main__':
    #modes: upload / download
    #schemes: sequential, delayed

    #ARGUMENTS
    repetitions = 5
    chunksizes = [1,4,5,8]
    means = [(10,8.8), (50,44), (100,88), (150,132)]
    #stddevs = [8.8, 44, 88, 132]
    serverload = [10,100,300]
    bandwith = [4,54,190,1000]

    #RESULT ARRAYS
    # Use a compound data type for structured arrays
    dt = np.dtype([('scheme', np.unicode_, 16), ('chunksize', np.int32), ('value', np.float64, (1,))])

    chunkresult = np.array([('seq', 1 , np.zeros(1)),('seq', 4 , np.zeros(1)),
                     ('seq', 5 , np.zeros(1)),('seq', 8 , np.zeros(1)),
                     ('del', 1 , np.zeros(1)),('del', 4 , np.zeros(1)),
                     ('del', 5 , np.zeros(1)) ,('del', 8 , np.zeros(1))], dtype=dt)

    dt = np.dtype([('scheme', np.unicode_, 16), ('mean', np.int32), ('value', np.float64, (repetitions,))])
    rttresult = np.array([('seq', 10 , np.zeros(repetitions)),('seq', 50 , np.zeros(repetitions)),
                          ('seq', 100 , np.zeros(repetitions)),('seq', 150 , np.zeros(repetitions)),
                          ('del', 10 , np.zeros(repetitions)),('del', 50 , np.zeros(repetitions)),
                          ('del', 100 , np.zeros(repetitions)) ,('del', 150 , np.zeros(repetitions))], dtype=dt)

    dt = np.dtype([('scheme', np.unicode_, 16), ('bandwith', np.int32), ('value', np.float64, (1,))])
    bandwithresult = np.array([('seq', 4 , np.zeros(1)),('seq', 54 , np.zeros(1)),
                                ('seq', 190 , np.zeros(1)),('seq', 1000 , np.zeros(1)),
                                ('del', 4 , np.zeros(1)),('del', 54 , np.zeros(1)),
                               ('del', 190 , np.zeros(1)),('del', 1000 , np.zeros(1))], dtype=dt)
    #Other
    rtt100 = []
    for i in range(1000):
        rtt100.append(100)



    #+++++++++++++++++++++Chunks++++++++++++++++++++++++++++++++++++++++++

    for size in chunksizes:
        clientq = queue.Queue()
        serverq = queue.Queue()
        ackq = queue.Queue()

        #++++++++++++++++++++++Sequential++++++++++++++++++++++++++++++

        s = Server(size, ackq, clientq, serverq, "receive" , "sequential" , rtt100, 10)
        c = Client(size, ackq, clientq, serverq, "send", "sequential")

        s.setName("Server")
        c.setName("Client")
        s.start()
        c.start()
        c.join()

        while True:
            if not c.is_alive():
                delay = s.get_delay()
                chunkresult['value'][:,0][np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['chunksize'] == size)] = delay
                s.join()

                break
                #sys.exit()

        #++++++++++++++++++++++Delayed++++++++++++++++++++++++++++++
        clientq = queue.Queue()
        serverq = queue.Queue()
        ackq = queue.Queue()


        s = Server(size, ackq, clientq, serverq, "receive" , "delayed" , rtt100, 10, 2)
        c = Client(size, ackq, clientq, serverq, "send", "delayed", 2)

        s.setName("Server")
        c.setName("Client")
        s.start()
        c.start()
        c.join()

        while True:
            if not c.is_alive():
                delay = s.get_delay()
                chunkresult['value'][:,0][np.logical_and(chunkresult['scheme'] == 'del', chunkresult['chunksize'] == size)] = delay
                s.join()

                break

    #+++++++++++++++++++++RTT++++++++++++++++++++++++++++++++++++++++++

    for x in range(repetitions):
        print(x)

        for value in means:

            lower, upper = 1, 1000
            mu, sigma = value[0], value[1]
            X = stats.truncnorm(
            (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
            # N = stats.norm(loc=mu, scale=sigma)
            rtt = X.rvs(size=1000)

            #++++++++++++++++++++++Sequential++++++++++++++++++++++++++++++
            clientq = queue.Queue()
            serverq = queue.Queue()
            ackq = queue.Queue()

            s = Server(4, ackq, clientq, serverq, "receive" , "sequential" , rtt, 10)
            c = Client(4, ackq, clientq, serverq, "send", "sequential")

            s.setName("Server")
            c.setName("Client")
            s.start()
            c.start()
            c.join()

            while True:
                if not c.is_alive():
                    delay = s.get_delay()
                    rttresult['value'][:,x][np.logical_and(rttresult['scheme'] == 'seq', rttresult['mean'] == value[0])] = delay
                    s.join()
                    break
                    #sys.exit()

            #++++++++++++++++++++++Delayed++++++++++++++++++++++++++++++

            clientq = queue.Queue()
            serverq = queue.Queue()
            ackq = queue.Queue()

            s = Server(4, ackq, clientq, serverq, "receive" , "delayed" , rtt, 10,2)
            c = Client(4, ackq, clientq, serverq, "send", "delayed", 2)

            s.setName("Server")
            c.setName("Client")
            s.start()
            c.start()
            c.join()

            while True:
                if not c.is_alive():
                    delay = s.get_delay()
                    rttresult['value'][:,x][np.logical_and(rttresult['scheme'] == 'del', rttresult['mean'] == value[0])] = delay
                    s.join()
                    break



    #+++++++++++++++++++++Bandwith++++++++++++++++++++++++++++++++++++++++++
    for speed in bandwith:
        print(speed)
        #++++++++++++++++++++++Sequential++++++++++++++++++++++++++++++
        clientq = queue.Queue()
        serverq = queue.Queue()
        ackq = queue.Queue()

        s = Server(4, ackq, clientq, serverq, "receive" , "sequential" , rtt100, 10, 1, speed)
        c = Client(4, ackq, clientq, serverq, "send", "sequential")

        s.setName("Server")
        c.setName("Client")
        s.start()
        c.start()
        c.join()

        while True:
            if not c.is_alive():
                delay = s.get_delay()
                bandwithresult['value'][:,0][np.logical_and(bandwithresult['scheme'] == 'seq', bandwithresult['bandwith'] == speed)] = delay
                s.join()

                break
                #sys.exit()

        #++++++++++++++++++++++Delayed++++++++++++++++++++++++++++++

        clientq = queue.Queue()
        serverq = queue.Queue()
        ackq = queue.Queue()

        s = Server(4, ackq, clientq, serverq, "receive" , "delayed" , rtt100, 10, 2,speed)
        c = Client(4, ackq, clientq, serverq, "send", "delayed", 2)

        s.setName("Server")
        c.setName("Client")
        s.start()
        c.start()
        c.join()

        while True:
            if not c.is_alive():
                delay = s.get_delay()
                bandwithresult['value'][:,0][np.logical_and(bandwithresult['scheme'] == 'del', bandwithresult['bandwith'] == speed)] = delay
                s.join()

                break

    ####Graphs#####################

    for size in chunksizes:
        chunkseq = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['chunksize'] == size)]
        chunkdel = chunkresult[np.logical_and(chunkresult['scheme'] == 'del', chunkresult['chunksize'] == size)]
        print(chunkseq)
        print(chunkdel)

    for speed in bandwith:
        bandwithseq = bandwithresult[np.logical_and(bandwithresult['scheme'] == 'seq', bandwithresult['bandwith'] == speed)]
        bandwithdel = bandwithresult[np.logical_and(bandwithresult['scheme'] == 'del', bandwithresult['bandwith'] == speed)]
        print(bandwithseq)
        print(bandwithdel)

    titles = []
    rttseqmeans = [] #np.array(np.zeros(repetitions*2))
    rttseqstds = [] #np.array(np.zeros(repetitions*2))
    rttdelmeans = []
    rttdelstds = []

    for mean in means:
        titles.append(str(mean)+"seq")
        titles.append(str(mean)+"del")
        rttseq = rttresult[np.logical_and(rttresult['scheme'] == 'seq', rttresult['mean'] == mean[0])]
        rttdel = rttresult[np.logical_and(rttresult['scheme'] == 'del', rttresult['mean'] == mean[0])]

        rttseqmean = np.mean(rttseq['value'])
        rttdelmean = np.mean(rttdel['value'])
        rttseqmeans.append(rttseqmean)
        rttdelmeans.append(rttdelmean)

        rttseqstd = np.std(rttseq['value'])
        rttdelstd = np.std(rttdel['value'])
        rttseqstds.append(rttseqstd)
        rttdelstds.append(rttdelstd)


    # print(titles)
    # print(rttmeans)
    # print(rttstds)
    titles = np.array(titles)
    rttseqmeans = np.array(rttseqmeans)
    rttdelmeans = np.array(rttdelmeans)
    rttseqstds = np.array(rttseqstds)
    rttdelstds = np.array(rttdelstds)

    print(titles)
    print(rttseqmeans)
    print(rttdelmeans)
    print(rttseqstds)
    print(rttdelstds)

    x_pos = np.arange(len(rttseqmeans))
    width = 0.35 #width of the bars

    fig, ax = plt.subplots()
    seqbar = ax.bar(x_pos, rttseqmeans, width, yerr=rttseqstds, align='center', alpha=0.5, ecolor='black', capsize=10)
    delbar = ax.bar(x_pos + width, rttdelmeans, width , yerr=rttdelstds, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Time (ms)')
    ax.set_xticks(x_pos + width / 2)
    #ax.set_xticklabels(titles)
    ax.set_xticklabels(('10', '50', '100', '150'))
    ax.set_title('RTTs')
    ax.yaxis.grid(True)
    ax.legend((seqbar[0], delbar[0]), ('Sequential', 'Delayed'))
    # Save the figure and show
    plt.tight_layout()
    plt.savefig('bar_plot_with_error_bars.png')
    plt.show()