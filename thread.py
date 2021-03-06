import _thread
import time
import machine
import gc
import micropython
import pycom

keep_going = True

mpy_heap_free = gc.mem_free()
mpy_stack_used = micropython.stack_use()
internal_heap_free = pycom.get_free_heap()[0]
external_heap_free = pycom.get_free_heap()[1]

def mem():
    global mpy_heap_free, mpy_stack_used, internal_heap_free, external_heap_free

    # machine.info()

    #print("MPy heap free=", gc.mem_free(), "alloc=", gc.mem_alloc(), "total=", gc.mem_alloc() + gc.mem_free(), "diff=", mpy_heap_free - gc.mem_free())
    # micropython.mem_info()
    print("MPy heap free=     {:>8} diff={:>6}".format(gc.mem_free(),gc.mem_free() - mpy_heap_free))
    print("MPy stack used=    {:>8} diff={:>6}".format(micropython.stack_use(), micropython.stack_use() - mpy_stack_used))
    print("internal heap free={:>8} diff={:>6}".format(pycom.get_free_heap()[0], pycom.get_free_heap()[0] - internal_heap_free))
    print("external heap free={:>8} diff={:>6}".format(pycom.get_free_heap()[1], pycom.get_free_heap()[1] - external_heap_free))

    mpy_heap_free = gc.mem_free()
    mpy_stack_used = micropython.stack_use()
    internal_heap_free = pycom.get_free_heap()[0]
    external_heap_free = pycom.get_free_heap()[1]



def th_func(delay, id):
    # if id == 0:
    #     print("Start thread in thread %d" %(id))
    #     _thread.start_new_thread(th_func, (delay+1,1000+id))
    ct = 0
    while keep_going:
        time.sleep(delay)
        print('id=%d\t ct=%d' % (id, ct) )
        ct += 1
    print('id=%d\t ct=%d --- end' % (id, ct) )


# create threads with increasing delays
def thread_test():
    mem()
    n = 24
    # GPy base core dumps at 25 in safe boot mode
    # , or 21?
    print("Starting %d threads...." %(n))
    for i in range(n):
        _thread.start_new_thread(th_func, (i + 1, i))
        print(i)
        time.sleep(0.2)
        #achine.info()
        mem()

    if False:
        keep_going = False

if __name__ == "__main__":
    # machine.info()
    print("start")
    try:
        thread_test()
    except Exception as e:
        print("Exception during thread_test:", e)
    print("sleep")
    time.sleep(5)
    print("end")
    keep_going = False
