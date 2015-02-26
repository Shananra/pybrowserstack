import pybrowserstack.avail_platforms as platforms
from pybrowserstack.platform_utils import *
import difflib,colorama
from colorama import Fore, Back, Style

class platform(object):
    browser = "IE"
    browser_version = "11"
    os = "Windows"
    os_version = "8"
    resolution = ""
    device = "desktop"
    
    def __str__(self):
        return "<%(device)s Browser Object> OS: %(os)s %(os_version)s Browser: %(browser)s %(version)s" % {
                    'device':self.device.title(),
                    'os':self.os,
                    'browser':self.browser,
                    'version': self.browser_version if self.device == 'desktop' else '',
                    'os_version':self.os_version
                }

class desktop_mixin(object):

    #def __init__(self):

    def get_latest(self,mylist,amount=1):
        mylist.sort(key=float)
        return mylist[-amount:]

    def get_generic(self,versions=1,version=None,resolution=None):
        myplatform = getattr(platforms,self.platform)
        myversions = []
        if version == None:
            myversions = self.get_latest(myplatform[self.os_version.lower().replace('.','_')][self.browser.lower()],amount=versions)
        else:
            if version not in myplatform[self.os_version][self.browser.lower()]:
                raise Exception("Provided version is not available for "+self.browser)
            myversions.append(version)
        for myversion in myversions:
            self.setcap(myversion,resolution)

    def setcap(self,myversion,resolution):
        thisplatform = platform()
        thisplatform.browser = self.browser
        thisplatform.browser_version = myversion
        thisplatform.os = self.os
        thisplatform.os_version = self.os_version
        thisplatform.device = self.device
        if self.device == "desktop":
            thisplatform.resolution = self.get_resolution(resolution)
        setcap(thisplatform)
    
    def get_resolution(self,resolution):
        myplatform = getattr(platforms,self.platform)
        resolutions = myplatform['res']
        bres = resolution
        if resolution == None:
            return resolutions[0][0]+"x"+resolutions[0][1]
        resolution = resolution.split('x')
        widths = range(len(resolutions) - 1)
        heights = range(len(resolutions) - 1)
        myorder = range(len(resolutions) - 1)
        widths = sorted(widths, key=lambda x: abs(int(resolutions[x][0]) - int(resolution[0])))
        heights = sorted(heights, key=lambda x: abs(int(resolutions[x][1]) - int(resolution[1])))
        myorder = sorted(myorder, key=lambda x: heights.index(x)+widths.index(x))
        resolution = resolutions[myorder[0]][0]+'x'+resolutions[myorder[0]][1]
        if resolution != bres:
            print(warn("Warning!")+" The resolution %(bres)s is not available, using %(resolution)s instead." % {'bres':bres,'resolution':resolution})
        return resolution
    def all(self,versions=1,resolution=None):
        myplatform = getattr(platforms,self.platform)
        for mybrowser in myplatform[self.os_version.lower().replace('.','_')]:
            getattr(self,mybrowser)(versions,resolution=resolution)
    def __call__(self,versions=1,resolution=None):
        self.all(versions=versions,resolution=resolution)
    def ie(self,versions=1,version=None,resolution=None):
        self.browser = "IE"
        self.get_generic(versions=versions,version=version,resolution=resolution)

    def firefox(self,versions=1,version=None,resolution=None):
        self.browser = "Firefox"
        self.get_generic(versions=versions,version=version,resolution=resolution)
    def safari(self,versions=1,version=None,resolution=None):
        self.browser = "Safari"
        self.get_generic(versions=versions,version=version,resolution=resolution)
    def chrome(self,versions=1,version=None,resolution=None):
        self.browser = "Chrome"
        self.get_generic(versions=versions,version=version,resolution=resolution)
    def opera(self,versions=1,version=None,resolution=None):
        self.browser = "Opera"
        self.get_generic(versions=versions,version=version,resolution=None)


class device_mixin(object):
    vendors = []
    def __call__(self):
        for i in getattr(platforms,self.device_type):
            getattr(self,i.lower().replace(' ','_'))()
    def __getattr__(self,name):
        print(name)
        name = name.lower()
        if name not in self.vendors:
            passme = {'bname':name}
            name = sorted(self.vendors, key=lambda x: difflib.SequenceMatcher(None, x, name).ratio())[0].lower()
            passme['aname'] = name
            print(warn("Warning!")+" The vendor %(bname)s was not found, using %(aname)s instead." % passme)
        return getattr(self,name)


class device_obj(object):
    vendor = "Apple"
    devices = []
    device_type = "mobile"
    def __init__(self,vendor,device_type):
        self.vendor = vendor
        self.devices = getattr(platforms,device_type)[vendor]
        self.device_type = device_type
    
    def setcap(self,mydevice):
        thisplatform = platform()
        thisplatform.browser = mydevice
        thisplatform.browser_version = ''
        thisplatform.os = 'MAC' if self.vendor=='Apple' else 'ANDROID'
        thisplatform.os_version = ''
        thisplatform.device = self.device_type
        thisplatform.vendor = self.vendor
        setcap(thisplatform)
    def __call__(self):
        self.setcap(self.devices[0])
    def __getattr__(self,name):
        if name not in self.devices:
            passme = {'bname':name}
            name = sorted(self.devices, key=lambda x: difflib.SequenceMatcher(None, x, name).ratio())[0]
            passme['aname'] = name
            print(warn("Warning!")+" The device %(bname)s was not found, using %(aname)s instead." % passme)
        self.setcap(name)
        return lambda: None

class tablets(device_mixin):
    device_type = 'tablet'
    def __init__(self):
        for i in platforms.tablet:
            setattr(self,i.lower().replace(' ','_'),device_obj(i,'tablet'))
            self.vendors.append(i)
    def all(self):
        pass


class mobile(device_mixin):
    device_type = 'mobile'
    def __init__(self):
        for i in platforms.mobile:
            setattr(self,i.lower().replace(' ','_'),device_obj(i,'mobile'))
            self.vendors.append(i)

class desktop(object):
    def __init__(self,parent):
        self.parent = parent
    def __call__(self):
        for i in get_avail_mixins():
            getattr(self.parent,i)()
    def __getattr__(self,name):
        mymixins = get_avail_mixins()
        if name not in mymixins:
            passme = {'bname':name}
            name = sorted(mymixins, key=lambda x: difflib.SequenceMatcher(None, x, name).ratio())[0]
            passme['aname'] = name
            print(warn("Warning!")+" The desktop device %(bname)s was not found, using %(aname)s instead." % passme)
        return getattr(self.parent,name)

class windows_7(desktop_mixin):
    os = 'Windows'
    os_version = '7'
    browser_version = '10'
    device = "desktop"
    platform = 'win'

class windows_xp(desktop_mixin):
    os = 'Windows'
    os_version = 'xp'
    browser_version = '8'
    device = "desktop"
    platform = 'win'

class windows_8(desktop_mixin):
    os = 'Windows'
    os_version = '8'
    browser_version = '10'
    device = "desktop"
    platform = 'win'

class windows_8_1(desktop_mixin):
    os = 'Windows'
    os_version = '8.1'
    browser_version = '11'
    device = "desktop"
    platform = 'win'

class yosemite(desktop_mixin):
    os = 'OS X'
    os_version = 'Yosemite'
    browser_version = '8.0'
    device = "desktop"
    platform = 'osx'

class mavericks(desktop_mixin):
    os = 'OS X'
    os_version = 'Mavericks'
    browser_version = '7.0'
    device = "desktop"
    platform = 'osx'

class mountainlion(desktop_mixin):
    os = 'OS X'
    os_version = 'Mountain Lion'
    browser_version = '6.1'
    device = "desktop"
    platform = 'osx'

class lion(desktop_mixin):
    os = 'OS X'
    os_version = 'Lion'
    browser_version = '6.0'
    device = "desktop"
    platform = 'osx'

class snowleopard(desktop_mixin):
    os = 'OS X'
    os_version = 'Snow Leopard'
    browser_version = '5.1'
    device = "desktop"
    platform = 'osx'

_avail_mixins = [cls.__name__ for cls in vars()['desktop_mixin'].__subclasses__()]
def get_avail_mixins():
    return _avail_mixins
def warn(mystr):
    return Fore.YELLOW+mystr+Style.RESET_ALL
