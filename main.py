import time
from datetime import datetime

from pyhue import Hue
from ouimeaux.environment import Environment
from ouimeaux.subscribe import SubscriptionRegistry

registry = SubscriptionRegistry()

def on_switch(switch):
    pass

def on_motion(motion):
    pass

env = Environment(on_switch, on_motion)

env.start()

ms = env.list_motions()
ss = env.list_switches()

m = ms[0]

m = env.get_motion(ms[0])
ss = [env.get_switch(s) for s in ss]

h = Hue()
ls = h.lights
print ls

def updated():
    t = time.localtime()
    n = datetime.now()
    print '*' * 100
    print n.strftime('%Y-%m-%d %H:%M:%S')
    print time.strftime("%A", t)
    if int(n.strftime('%H')) >= 18 or int(n.strftime('%H')) < 7:
        for l in ls:
            l.on(0)
    else:
        for l in ls:
            l.off(0)

m.on_device_updated_on = updated

registry.register(m)

env.wait()
