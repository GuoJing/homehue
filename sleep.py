from pyhue import Hue

h = Hue()
ls = h.lights

sleep = dict(sofa=[0.6109, 0.3683],
             room=[0.6109, 0.3683],
             bed=[0.6109, 0.3683])

for l in ls:
    if l.state.on:
        xy = sleep.get(l.name.lower())
        l.on()
        d = dict(xy=xy, bri=31)
        l.set_state(d)
