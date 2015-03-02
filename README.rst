pybrowserstack extends the unittest framework to make selenium/browserstack automated tests really easy.

To install, simply run

::
    
    pip install pybrowserstack

Example:
::
    
    import pybrowserstack
    import unittest
    
    class SeleniumTestCase(pybrowserstack.testBase,unittest.TestCase):
    
        def setUp(self):
            self.api_keys['user'] = '<your username>'
            self.api_keys['pass'] = '<api key provided by browserstack>'
            self.workers = 2
            self.windows_7.ie()
            self.windows_8.firefox()
            self.mobile()
    
        @pybrowserstack.browserstack
        def test_firefox(self):
            self.driver.get("http://google.com")
            print(self.driver.title)
    
    if __name__ == '__main__':
        unittest.main()

The above example will use two workers and test IE on windows 7, firefox on windows 8, and one browser on each mobile device available. The test_firefox block will be run, which will print "Google" once for each test.

In the setUp method, include all of the browsers you want to run. To include the latest version of every browser, you could use the following shortcut:

::

    self.desktop()
    self.mobile()
    self.tablet()


To include all windows 7 browsers, you could run:

::
    
    self.desktop.windows_7()

To include only the newest available IE on windows 7:

::

    self.desktop.windows_7.ie()

for an older version of firefox, say version 32 on Windows 8 you could run:

::

    self.desktop.windows_8.firefox(version=32)

If you would like to test on the three newest versions of chrome on OS X Yosemite, you could try this:

self.desktop.yosemite.chrome(versions=3)

In order to specify your resolution, pass it in as a parameter. For example:

::

    self.desktop.windows_8.chrome(resolution='1024x768')

If the resolution you specified could not be found, pybrowserstack will find the closest match and throw a warning. Note that many of the above parameters are not available on mobile. 

You can test on every IOS tablet device with this command:

::

    self.tablet.apple()

Or, if you simply want to test on the iphone 5

::

    self.mobile.apple.iphone5()


If you would like to run through a local proxy, start your local session as you normally would (using ./BrowserStackLocal ACCESS_KEY localhost,3000,0) then, in your setUp method, include these lines:

::
    
    self.local = True
    self.local_id = '<your test id>'

Need other custom options? Add those to the self._global_caps dictionary
