import time
from datetime import datetime

from pyhue import Hue
from ouimeaux.environment import Environment
from ouimeaux.subscribe import SubscriptionRegistry

registry = SubscriptionRegistry()

env = Environment(with_cache=False)

env.start()

env.discover(3)

ms = env.list_motions()
ss = env.list_switches()

m = ms[0]

m = env.get_motion(ms[0])
ss = [env.get_switch(s) for s in ss]

h = Hue()
ls = h.lights
print ls

sunset = dict(sofa=[0.5543, 0.4098],
              room=[0.5452, 0.4164],
              bed=[0.5848, 0.3872])

def updated():
    t = time.localtime()
    n = datetime.now()
    print '*' * 100
    print n.strftime('%Y-%m-%d %H:%M:%S')
    print time.strftime("%A", t)
    if True:
    #if int(n.strftime('%H')) >= 19 or int(n.strftime('%H')) < 7:
        for l in ls:
            if not l.state.on:
                xy = sunset.get(l.name.lower())
                print xy
                if not xy:
                    print 'x' * 100
                    print 'xy is not configured'
                    xy = [0.5543, 0.4098]
                l.on()
                d = dict(xy=xy, bri=255)
                l.set_state(d)
    else:
        pass
        #for l in ls:
        #    l.off()

m.on_device_updated_on = updated

registry.register(m)

env.wait()
