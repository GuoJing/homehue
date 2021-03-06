import logging
from urlparse import urlparse

import requests

from ouimeaux.service import Service
from ouimeaux.xsd import device as deviceParser


log = logging.getLogger(__name__)


class UnknownService(Exception): pass


class Device(object):
    def __init__(self, url):
        self._state = None
        base_url = url.rsplit('/', 1)[0]
        self.host = urlparse(url).hostname
        xml = requests.get(url)
        self._config = deviceParser.parseString(xml.content).device
        sl = self._config.serviceList
        self.services = {}
        for svc in sl.service:
            svcname = svc.get_serviceType().split(':')[-2]
            service = Service(svc, base_url)
            service.eventSubURL = base_url + svc.get_eventSubURL()
            self.services[svcname] = service
            setattr(self, svcname, service)

    def _update_state(self, value):
        if int(value) == self._state:
            return
        self._state = int(value)
        if value:
            self.on_device_updated_on()
        else:
            self.on_device_updated_off()

    def on_device_updated_on(self):
        pass

    def on_device_updated_off(self):
        pass

    def get_state(self, force_update=False):
        """
        Returns 0 if off and 1 if on.
        """
        if force_update or self._state is None:
            return int(self.basicevent.GetBinaryState()['BinaryState'])
        return self._state

    def get_service(self, name):
        try:
            return self.services[name]
        except KeyError:
            raise UnknownService(name)

    def list_services(self):
        return self.services.keys()

    def explain(self):
        for name, svc in self.services.iteritems():
            print name
            print '-' * len(name)
            for aname, action in svc.actions.iteritems():
                print "  %s(%s)" % (aname, ', '.join(action.args))
            print

    @property
    def model(self):
        return self._config.get_modelDescription()

    @property
    def name(self):
        return self._config.get_friendlyName()

    @property
    def serialnumber(self):
        return self._config.get_serialNumber()


def test():
    device = Device("http://10.42.1.102:49152/setup.xml")
    print device.get_service('basicevent').SetBinaryState(BinaryState=1)


if __name__ == "__main__":
    test()

