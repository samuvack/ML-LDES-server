from multiprocessing import Process, Queue, Value, Manager
from ctypes import c_bool
from threading import Thread


ps = []

def yourFunc(pause, budget):
    while True:
        print(budget.value, pause.value)
        ##set value
        pause.value = True  


def multiProcess(threads, pause, budget):
    for _ in range(threads):
        t = Thread(target=yourFunc(), args=(pause, budget,)) 
        t.start()
        ts.append(t)
        time.sleep(3)

if __name__ == '__main__':
    pause = Value(c_bool, False)
    budget = Value('i', 5000)

    for i in range(2):
        p = Process(target=multiProcess, args=(2, pause, budget))
        p.start()
        ps.append(p) 