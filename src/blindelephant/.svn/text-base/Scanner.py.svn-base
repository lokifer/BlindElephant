import Fingerprinters as wafp
import Loggers as wal
from optparse import OptionParser
import datetime

class ScannerResult(object):
    def __init__(self, url):
        self.url = url
        self.apps = {}
        self.plugins = {}
    
    def print_results(file):
        pass
    
    def __str__(self):
        str = ""
        str += "Scanner Results for %s\n" % url
        
        for app, vers in self.apps.iteritems():
            verstrs = [v.vstring for v in vers]
            str += "  - %s: %s\n" % (app, verstrs)
            
            if self.plugins.has_key(app):
                for plugin, vers in self.plugins[app].iteritems():
                    verstrs = [v.vstring for v in vers]
                    str += "    -- %s: %s\n" % (plugin, verstrs)
        return str
        

        
    

class Scanner(object):
    def __init__(self, url, scan_plugins=False):
        self.url = url
        self.scan_plugins = scan_plugins
        self.result = ScannerResult(url)
        self.logger = wal.FileLogger(open("/dev/null", "w"))
        self.app_guesser = wafp.WebAppGuesser(url, logger=self.logger)
    
    def scan(self):
        
        possible_apps = self.app_guesser.guess_apps()
        
        for app_name in possible_apps:
            fp = wafp.WebAppFingerprinter(self.url, app_name, logger=self.logger)
            self.result.apps[app_name] = fp.fingerprint()
        
        if self.scan_plugins:
            for app_name in possible_apps:
                pg = wafp.PluginGuesser(self.url, app_name)
                self.result.plugins[app_name] = {}
                
                possible_plugins = pg.guess_plugins()
                
                for plugin_name in possible_plugins:
                    pfp = wafp.PluginFingerprinter(self.url, app_name, plugin_name, logger=self.logger)
                    self.result.plugins[app_name][plugin_name] = pfp.fingerprint()



if __name__ == '__main__':
    USAGE = "usage: %prog [options] url"
    EPILOGUE = """Check a URL for any webapps supported by BlindElephant, and 
               fingerprint any found. With optional -p, also detect and fingerprint
               plugins (not all supported apps have supported plugins)."""

    parser = OptionParser(usage=USAGE, epilog=EPILOGUE)
    parser.add_option("-p", "--plugins", action="store_true", help="Detect and fingerprint plugins too")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        print "Error: url is required argument\n"
        parser.print_help()
        quit()

    url = args[0].strip("/")
    
    start = datetime.datetime.now()
    s = Scanner(url, options.plugins)
    s.scan()
    finish = datetime.datetime.now()
    print s.result
    print "Fingerprint time: ", finish - start
    
    

                
        