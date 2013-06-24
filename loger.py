import os
from datetime import datetime

print datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

rs = os.popen('tail -n 2 /home/pi/.home_hue').readlines()

rs = [r.replace('\n', '') for r in rs]

try:
    for r in rs:
        if 'IndexError' in r:
            os.popen('/etc/init.d/homehue stop')
except:
    pass

try:
    l1, l2 = rs[0], rs[1]
    l1 = ''.join(l1.split(' ')[5:-1])
    l2 = ''.join(l2.split(' ')[5:-1])
    print l1
    print l2
    if l1 == l2 and ('200' in l1) and ('200' in l2):
        r = os.system('/etc/init.d/homehue stop')
        print r
        print 'stop'
except Exception, e:
    print 'Exception %s' % e
    
