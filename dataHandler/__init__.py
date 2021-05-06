import sched,time

from .views import load

def lol():
    # print('kek')
    s = sched.scheduler(time.time,time.sleep)
    user_id = 1
    while user_id <20   :
        s.enter(1,1,load,(user_id,))
        s.run()
        user_id += 1
        # set_interval(p,1,i)

lol()
