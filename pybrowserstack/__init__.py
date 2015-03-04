import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import concurrent.futures
import pybrowserstack.platform_mixins

from pybrowserstack.platform_utils import *
import time

def browserstack(myfunc):

    def worker(mycap,tester):
        global has_screenshot
        has_screenshot = False
        tester.driver = webdriver.Remote(command_executor='http://%(user)s:%(pass)s@hub.browserstack.com:80/wd/hub' % tester.api_keys,desired_capabilities=mycap)
        bk_save_screenshot = tester.driver.save_screenshot
        
        def new_save_screenshot(*args):
            global has_screenshot
            has_screenshot = True
            bk_save_screenshot(*args)
        tester.driver.save_screenshot = new_save_screenshot
        myfunc(tester)
        if not has_screenshot:
            bk_save_screenshot('saved.png')
        tester.driver.quit()
        return True
    def runjobs(tester,mycaps,retry=0):
        retrycaps = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=tester.workers) as executor:
            future_worker = {executor.submit(worker,tester.gen_cap(mycap),tester): mycap for mycap in mycaps}
            for future in concurrent.futures.as_completed(future_worker):
                mycap = future_worker[future]
                try:
                    data = future.result()
                except Exception as exc:
                    if 'sessions are currently being used' in str(exc):
                        if retry < 3:
                            print('Too many sessions are being used. Will retry: '+str(mycap))
                            retrycaps.append(mycap)
                        else:
                            print('generated an exception: %s' % (exc,))
                else:
                    print("Completed "+str(mycap))
        if retry < 3 and len(retrycaps) > 0:
            print("Waiting 30 seconds before retrying failed targets...")
            time.sleep(30)
            runjobs(tester,mycaps,retry+1)
    def deco(tester,retry=0):
        if tester.api_keys['user'] == '' or tester.api_keys['pass'] == '':
            raise Exception("Username and api key are required")
        runjobs(tester,getcaps())
    return deco

class testBase(object):
    
    test = "one"
    _global_caps = {
    }
    local = False
    local_id = 'MyTest'
    workers = 1
    api_keys = {'user':'','pass':''}


    def __init__(self,*args,**kargs):
        for i in platform_mixins.get_avail_mixins():
            setattr(self,i,getattr(platform_mixins,i)())
        self.tablets = platform_mixins.tablets()
        self.tablet = self.tablets#make this an alias
        self.mobile = platform_mixins.mobile()
        self.desktop = platform_mixins.desktop(self)
        self.desktops = self.desktop#also an alias
        super(testBase, self).__init__(*args, **kargs)

    def show(self):
        mycaps = getcaps()
        print("%(num)s browser objects found" % {'num':len(mycaps)})
        for i in mycaps:
            print(str(i))
    


    def gen_cap(self,bobj):
        new_cap = {}
        if self.local:
            new_cap['browserstack.local'] = True
            new_cap['browserstack.localIdentifier'] = self.local_id
        if bobj.device == 'desktop':
            new_cap['os'] = bobj.os
            new_cap['browser'] = bobj.browser
            new_cap['os_version'] = bobj.os_version
            new_cap['browser_version'] = bobj.browser_version
        elif bobj.device in ['tablet','mobile']:
            if bobj.vendor == 'Apple':
                new_cap['device'] = bobj.browser
                new_cap['browserName'] = 'iPhone' if bobj.device == 'mobile' else 'iPad'
            else:
                new_cap['device'] = bobj.vendor+' '+bobj.browser
                new_cap['browserName'] = 'android'
            new_cap['platform'] = bobj.os
        if bobj.resolution != '':
            new_cap['resolution'] = bobj.resolution
        for mycap in self._global_caps:
            new_cap[mycap] = self._global_caps[mycap]
            
        return new_cap

    
if __name__ == '__main__':
    mytest = testBase()
    mytest.windows_7.ie(resolution='1024x1024')
    #mytest.windows_8()
    mytest.mavericks.firefox(resolution='1281x1900')
    mytest.tablets()
    mytest.mobile.htcone()
    mytest.mobile.htc.htcone()
    mytest.show()
