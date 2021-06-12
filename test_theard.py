from multiprocessing import Queue

q2 = Queue(3)
for i in range(5):
    try:
        q2.put(i, block=True, timeout=1)
    except:
        print('消息队列已经满，现在有消息数量：%s'%(q.qsize()))
        print('~~~~~~~~~~~~~~~~~~~~~~')

while not q2.empty():
    print(q2.get())
print(q2.get())

from threading import Thread
from multiprocessing import Process

g_num =  100

def work1():
    global g_num
    for i in range(3):
        g_num+=1
    print('-----in work1,g_num is %d'%(g_num))

def work2():
    global g_num
    for i in range(3):
        g_num += 1
    print('-----in work2,g_num is %d'%(g_num))

if __name__ == '__main__':

    # t1 = Thread(target=work1)
    # t1.start()
    #
    # t2 = Thread(target=work2)
    # t2.start()

    #由于多线程可以共享全局变量，所以g_num由原来的100变成了106


    #多进程之间内存独立，不能够共享全局变量。如果通信的话，使用Queue
    p1 = Process(target=work1)
    p1.start()

    p2 = Process(target=work2)
    p2.start()
