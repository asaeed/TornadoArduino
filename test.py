
import multiprocessing
import time
import sys
import server

def daemon():
    print 'Starting:', multiprocessing.current_process().name
    time.sleep(3)
    print 'Exiting :', multiprocessing.current_process().name

def non_daemon():
    print 'Starting:', multiprocessing.current_process().name
    print 'Exiting :', multiprocessing.current_process().name

if __name__ == '__main__':
    d = multiprocessing.Process(name='tornadoServer', target=server.main)
    #d.daemon = True
    d.start()

    while True:
        pass