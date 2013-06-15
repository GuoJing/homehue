# -*- coding: utf-8 -*-
from config import DEFAULT_TRANSITIONTIME

try:
    from colorpy import colormodels
except:
    from warnings import warn
    warn('You should install colorpy, try pip install colorpy')

class HueControllerMixin:

    def set_state(self, state):
        raise Exception('you should rewrite set_state')

    def on(self, transitiontime=DEFAULT_TRANSITIONTIME):
        d = dict(on=True, transitiontime=transitiontime)
        if self._saved_state:
            d = self._saved_state
            self._saved_state = None
        return self.set_state(d)

    def off(self, transitiontime=DEFAULT_TRANSITIONTIME, save_state=True):
        '''
        SAVE STATE only work when the light is on
        '''
        d = dict(on=False, transitiontime=transitiontime)
        if save_state:
            self._saved_state = self.state_dict
        return self.set_state(d)

    def ct(self, ct, transitiontime=DEFAULT_TRANSITIONTIME):
        d = dict(ct=ct, transitiontime=transitiontime)
        return self.set_state(d)

    def cct(self, cct, transitiontime=DEFAULT_TRANSITIONTIME):
        return self.ct(1000000 / cct, transitiontime)

    def bri(self, bri, transitiontime=DEFAULT_TRANSITIONTIME):
        d = dict(bri=bri, transitiontime=transitiontime)
        return self.set_state(d)

    def toggle(self, transitiontime=DEFAULT_TRANSITIONTIME):
        if self.state and self.state.get(
                'state', None) and self.state['state'].get('on', None):
            self.off(transitiontime)
        else:
            self.on(transitiontime)

    def alert(self, type='select'):
        d = dict(alert=type)
        return self.set_state(d)

    def xy(self, x, y, transitiontime=DEFAULT_TRANSITIONTIME):
        d = dict(xy=[x, y], transitiontime=transitiontime)
        return self.set_state(d)

    def rgb(self, red, green=None, blue=None):
        return self._rgb_transfer(red, green, blue)

    def css(self, csshex):
        return self._rgb_transfer(csshex)

    def _rgb_transfer(self, red, green=None, blue=None,
            transitiontime=DEFAULT_TRANSITIONTIME):
        if isinstance(red, basestring):
            rstring = red
            red = int(rstring[1:3], 16)
            green = int(rstring[3:5], 16)
            blue = int(rstring[5:], 16)

        colormodels.init(
            phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
            phosphor_green=colormodels.xyz_color(0.4091, 0.518),
            phosphor_blue=colormodels.xyz_color(0.167, 0.04))
        xyz = colormodels.irgb_color(red, green, blue)
        xyz = colormodels.xyz_from_rgb(xyz)
        xyz = colormodels.xyz_normalize(xyz)
        d = dict(xy=[xyz[0], xyz[1]], transitiontime=transitiontime)
        return self.set_state(d)

    def effect(self, colorloop=True):
        d = dict(colorloop='none')
        if colorloop:
            d = dict(colorloop='colorloop')
        return self.set_state(d)

