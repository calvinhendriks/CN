from main.Server import Server
from main.Client import Client
import numpy as np
import scipy.stats as stats
from threading import Thread
import queue
import sys
import matplotlib.pyplot as plt
import os


if __name__ =='__main__':
    #modes: upload / download
    #schemes: sequential, delayed
    my_path = os.path.abspath(__file__)

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

    ############################################Graphs###########################################

    #####Chunksize#################
    chunkseq = []
    chunkdel = []
    for size in chunksizes:
        a = chunkresult[np.logical_and(chunkresult['scheme'] == 'seq', chunkresult['chunksize'] == size)]['value']
        #print(a[0][0])
        chunkseq.append(a[0][0])
        b = chunkresult[np.logical_and(chunkresult['scheme'] == 'del', chunkresult['chunksize'] == size)]['value']
        #print(b[0][0])
        chunkdel.append(b[0][0])
    print("chunksize seq", chunkseq)
    print("chunksize del", chunkdel)
    chunkseq = np.array(chunkseq)
    chunkdel = np.array(chunkdel)
    #Make array for percentage change above bars
    chunkdif = []
    for i in range(len(chunkseq)):
        x = (chunkdel[i] / chunkseq[i] )
        x = "{:.2%}".format(x)
        chunkdif.append(x)
    chunkdif = np.array(chunkdif)

    x_pos = np.arange(len(chunkseq))
    width = 0.35 #width of the bars
    fig, ax  = plt.subplots()
    chunkseqbar = ax.bar(x_pos, chunkseq, width, align='center', alpha=0.5, ecolor='black', capsize=10)
    chunkdelbar = ax.bar(x_pos + width, chunkdel, width , align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Time (ms)')
    ax.set_xticks(x_pos + width / 2)
    #ax.set_xticklabels(titles)
    ax.set_xticklabels(chunksizes)
    ax.set_title('Chunksizes')
    ax.yaxis.grid(True)
    ax.legend((chunkseqbar[0], chunkdelbar[0]), ('Sequential', 'Delayed'))
    for a,b,c in zip(x_pos + (width / 2), chunkdel, chunkdif):
        plt.text(a, b, c)
    # Save the figure and show
    plt.xlabel("Chunksizes (MB)")
    plt.tight_layout()
    plt.savefig('graphs/chunk_seq_del_graph.png')
    #plt.show()

    #####Bandwith#################
    bandwithseq = []
    bandwithdel = []
    for speed in bandwith:
        a = bandwithresult[np.logical_and(bandwithresult['scheme'] == 'seq', bandwithresult['bandwith'] == speed)]['value']
        bandwithseq.append(a[0][0])
        b = bandwithresult[np.logical_and(bandwithresult['scheme'] == 'del', bandwithresult['bandwith'] == speed)]['value']
        bandwithdel.append(b[0][0])
    print("bandwith seq", bandwithseq)
    print("bandwith del", bandwithdel)
    bandwithseq = np.array(bandwithseq)
    bandwithdel = np.array(bandwithdel)

    bandwithdif = []
    for i in range(len(bandwithseq)):
        x = (bandwithdel[i] / bandwithseq[i] )
        x = "{:.2%}".format(x)
        bandwithdif.append(x)
    bandwithdif = np.array(bandwithdif)

    indices = np.arange(1,len(bandwithseq))
    bandwithseq = np.take(bandwithseq,indices)
    bandwithdel = np.take(bandwithdel,indices)
    bandwithdif = np.take(bandwithdif,indices)

    print("bandwith seq", bandwithseq)
    print("bandwith del", bandwithdel)
    print(len(bandwithseq))
    print(len(bandwithdel))

    x_pos = np.arange(len(bandwithseq))
    print(x_pos)
    width = 0.35 #width of the bars
    fig, ax  = plt.subplots()
    bandwithseqbar = ax.bar(x_pos, bandwithseq, width, align='center', alpha=0.5, ecolor='black', capsize=10)
    bandwithdelbar = ax.bar(x_pos + width, bandwithdel, width , align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Time (ms)')
    ax.set_xticks(x_pos + width / 2)
    #ax.set_xticklabels(titles)

    ax.set_xticklabels(np.take(bandwith, indices))
    ax.set_title('Bandwith')
    ax.yaxis.grid(True)
    ax.legend((bandwithseqbar[0], bandwithdelbar[0]), ('Sequential', 'Delayed'))
    # Save the figure and show
    for a,b,c in zip(x_pos + (width / 2), bandwithdel, bandwithdif):
        plt.text(a, b, c)
    plt.xlabel("bandwith (mpbs)")
    plt.tight_layout()
    plt.savefig('graphs/bandwith_seq_del_graph.png')
    #plt.show()


    #####RTT########################
    titles = []
    rttseqmeans = []
    rttseqstds = []
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

    #Make array for percentage change above bars
    rttdif = []
    for i in range(len(rttseqmeans)):
        x = (rttdelmeans[i] / rttseqmeans[i] )
        x = "{:.2%}".format(x)
        rttdif.append(x)
    rttdif = np.array(rttdif)

    print(titles)
    print("rtt seq means" , rttseqmeans)
    print("rtt del means", rttdelmeans)
    print("rtt seq std", rttseqstds)
    print("rtt del std", rttdelstds)

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
    for a,b,c in zip(x_pos + (width / 2), rttseqmeans, rttdif):
        plt.text(a, b, c)
    # Save the figure and show
    plt.xlabel("Round-trip time (ms)")
    plt.tight_layout()
    plt.savefig('graphs/rtt_seq_del_graph(errorbars).png')
    #plt.show()