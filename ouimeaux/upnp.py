import logging

import gevent
from gevent import socket
from gevent.server import DatagramServer


log = logging.getLogger(__name__)


class UPnP(object):
    """
    Makes M-SEARCH requests, filters out non-WeMo responses, and calls a
    user-provided handler with the results.
    """

    def __init__(self, handler, mcast_ip='239.255.255.250', mcast_port=1900, bind=None):
        if bind is None:
            host = socket.gethostbyname(socket.gethostname())
            port = 54321
            bind = '{0}:{1}'.format(host, port)
        self.bind = bind
        self.mcast_ip = mcast_ip
        self.mcast_port = mcast_port
        self.clients = {}
        self._handler = handler

    def _response_received(self, message, address):
        log.debug("Received a response from {0}:{1}".format(*address))
        if address[0] not in self.clients:
            lines = message.splitlines()
            lines.pop(0) # HTTP status
            headers = {}
            for line in lines:
                try:
                    header, value = line.split(":", 1)
                    headers[header.lower()] = value.strip()
                except ValueError:
                    continue
            if (headers.get('x-user-agent', None) == 'redsonic'):
                log.info("Found WeMo at {0}:{1}".format(*address))
                self.clients[address[0]] = headers
                gevent.spawn(self._handler, address, headers)

    @property
    def server(self):
        """
        UDP server to listen for responses.
        """
        server = getattr(self, "_server", None)
        if server is None:
            log.debug("Binding datagram server to %s", self.bind)
            server = DatagramServer(self.bind, self._response_received)
            self._server = server
        return server

    def broadcast(self):
        """
        Send a multicast M-SEARCH request asking for devices to report in.
        """
        log.debug("Broadcasting M-SEARCH to %s:%s", self.mcast_ip, self.mcast_port)
        request = '\r\n'.join(("M-SEARCH * HTTP/1.1",
                               "HOST:{mcast_ip}:{mcast_port}",
                               "ST:upnp:rootdevice",
                               "MX:2",
                               'MAN:"ssdp:discover"',
                               "", "")).format(**self.__dict__)
        self.server.sendto(request, (self.mcast_ip, self.mcast_port))


def test():
    logging.basicConfig(level=logging.DEBUG)

    def handler(address, headers):
        print "I GOT ONE"
        print address, headers

    upnp = UPnP(handler)
    upnp.server.set_spawn(1)
    upnp.server.start()
    log.debug("Started server, listening for responses")
    with gevent.Timeout(2, KeyboardInterrupt):
        while True:
            try:
                upnp.broadcast()
                gevent.sleep(2)
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    test()
