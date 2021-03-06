import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import concurrent.futures
import pybrowserstack.platform_mixins

from pybrowserstack.platform_utils import *
import time,sys,pprint
pp = pprint.PrettyPrinter(indent=4)

def browserstack(myfunc):

    def worker(mycap, tester, has_failure):
        global has_screenshot
        if has_failure:
            return False
        print("starting...")
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
        try:
            tester.driver.quit()
        except:
            pass
        return True
    def runjobs(tester,mycaps,retry=0):
        retrycaps = []
        has_failure = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=tester.workers) as executor:
            future_worker = {executor.submit(worker,tester.gen_cap(mycap),tester,has_failure): mycap for mycap in mycaps}
            for future in concurrent.futures.as_completed(future_worker):
                mycap = future_worker[future]
                if has_failure:
                    retrycaps.append(mycap)
                    continue
                try:
                    data = future.result()
                except WebDriverException as exc:
                    if 'sessions are currently being used' in str(exc):
                        if tester.skip_on_multiple_failures and retry > 2:
                            print('Skipping '+str(mycap))
                        elif retry < 5:
                            print('Too many sessions are being used. Will retry: '+str(mycap))
                            retrycaps.append(mycap)
                            has_failure = True
                        else:
                            print('generated an exception: %s' % (exc,))
                    elif 'Session not started or terminated' in str(exc):
                        if tester.skip_on_multiple_failures and retry > 2:
                            print('Skipping '+str(mycap))
                        elif retry < 5:
                            print('Session not started, will retry: '+str(mycap))
                            retrycaps.append(mycap)
                            try:
                                tester.driver.quit()
                            except:
                                pass
                            time.sleep(60)
                    elif 'Could not start Browser' in str(exc):
                        if tester.skip_on_multiple_failures and retry > 2:
                            print('Skipping '+str(mycap))
                        if retry < 5:
                            print("Emulator failed to start, will retry: "+str(mycap))
                            retrycaps.append(mycap)
                    else:
                        print('Unknown remote exception, will retry: '+str(mycap))
                        print(str(exc))
                except:
                    # This means our test failed, it wasn't a problem on the remote end most likely.
                    try:
                        tester.driver.quit()
                    except:
                        pass
                    raise
                else:
                    print("Completed "+str(mycap))
                sys.stdout.flush()
        if retry < 5 and len(retrycaps) > 0:
            print("Devices remaining on this run: "+str(len(retrycaps)))
            pp.pprint([str(x) for x in retrycaps])
            print("Waiting 90 seconds before retrying failed targets...")
            time.sleep(90)
            runjobs(tester,retrycaps,retry+1)
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
    skip_on_multiple_failures = False

    def __init__(self,*args,**kargs):
        for i in platform_mixins.get_avail_mixins():
            setattr(self,i,getattr(platform_mixins,i)())
        self.tablets = platform_mixins.tablets()
        self.tablet = self.tablets#make this an alias
        self.mobile = platform_mixins.mobile()
        self.desktop = platform_mixins.desktop(self)
        self.desktops = self.desktop#also an alias
        super(testBase, self).__init__(*args, **kargs)

    def new_session(self):
        reset_caps()

    def show(self):
        mycaps = getcaps()
        print("%(num)s browser objects found" % {'num':len(mycaps)})
        for i in mycaps:
            print(str(i))
    


    def gen_cap(self,bobj):
        new_cap = {}
        if self.local:
            new_cap['browserstack.local'] = True
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
        self.browser = bobj
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
