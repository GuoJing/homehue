import urllib2
import socket
import json

socket.setdefaulttimeout(10)

def get_nupnp_info():
    response = urllib2.urlopen('http://www.meethue.com/api/nupnp', timeout=10)
    r = json.loads(response.read())
    return r

def get_id(device_index=0):
    info = get_nupnp_info()
    id = info[device_index].get('id')
    return str(id)

def get_internalipaddress(device_index=0):
    info = get_nupnp_info()
    internalipaddress = info[device_index].get('internalipaddress')
    return str(internalipaddress)

def get_macaddress(device_index=0):
    info = get_nupnp_info()
    macaddress = info[device_index].get('macaddress')
    return str(macaddress)

def get_hue(ip='', devicetype=''):
    from hue import Hue
    ip = ip or get_internalipaddress()
    return Hue(station_ip=ip, devicetype=devicetype)
