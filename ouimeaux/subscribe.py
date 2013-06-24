from collections import defaultdict
import logging
from xml.etree import cElementTree
from functools import partial

import requests
import gevent
from gevent import socket
from gevent.wsgi import WSGIServer


log = logging.getLogger(__name__)

NS = "{urn:schemas-upnp-org:event-1-0}"


class SubscriptionRegistry(object):
    def __init__(self):
        self._devices = {}
        self._callbacks = defaultdict(list)

    def register(self, device):
        log.info("Subscribing to basic events from %r", (device,))
        # Provide a function to register a callback when the device changes state
        device.register_listener = partial(self.on, device, 'BinaryState')
        self._devices[device.host] = device
        self._resubscribe(device.basicevent.eventSubURL)

    def _resubscribe(self, url, sid=None):
        headers = {'TIMEOUT': 'infinite'}
        if sid is not None:
            headers['SID'] = sid
        else:
            host = socket.gethostbyname(socket.gethostname())
            headers.update({
                "CALLBACK": '<http://%s:8989>' % host,
                "NT": "upnp:event"
            })

        try:
            response = requests.request(method="SUBSCRIBE", url=url,
                                    headers=headers)
            timeout = 50
            try:
                timeout = int(response.headers['timeout'].replace('Second-', ''))
            except:
                log.info("Error parse timeout")
                print "Error parse timeout"
                timeout = 50
            try:
                sid = response.headers['sid']
            except:
                log.info("Error parse sid")
                print "Error parse sid"
            gevent.spawn_later(timeout, self._resubscribe, url, sid)
        except:
            log.info("Error parse timeout")
            gevent.spawn_later(10, self._resubscribe, url, sid)

    def _handle(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        try:
            if environ['REMOTE_ADDR'] == '10.0.1.85':
                environ['REMOTE_ADDR'] = '10.0.1.5'
            device = self._devices[environ['REMOTE_ADDR']]
            doc = cElementTree.parse(environ['wsgi.input'])
            for propnode in doc.findall('./{0}property'.format(NS)):
                for property_ in propnode.getchildren():
                    self._event(device, property_.tag, property_.text)
        except Exception, e:
            pass
        yield '200'

    def _event(self, device, type_, value):
        for t, callback in self._callbacks.get(device, ()):
            if t == type_:
                callback(value)

    def on(self, device, type, callback):
        self._callbacks[device].append((type, callback))

    @property
    def server(self):
        """
        UDP server to listen for responses.
        """
        server = getattr(self, "_server", None)
        if server is None:
            server = WSGIServer(('', 8989), self._handle)
            self._server = server
        return server

