"""Fingerprinter and Guesser objects for WebApps and their plugins"""
import DifferencesTables as wadt
import Configuration as wac
import FileMassagers as wafm
import FingerprintUtils as wafu
from Loggers import FileLogger

import BaseHTTPServer
from httplib import HTTPException 
import urllib2
import hashlib
import itertools
import os

#Number of consecutive low-level communication failures to tolerate before giving up
HOST_DOWN_THRESHOLD = 2

# TODO:
# - implement winnowing
# - stop early on consistent and accurate results + make this configurable
    

class WebAppFingerprinter(object):
    """Class that encapsulates the data and functions needed to use a 
    BlindElephant fingerprint db to attempt to get the version of a web
    app.
    """
    
    def __init__(self, url, app_name, num_probes=15, logger=FileLogger(), winnow=False):
        """Expects the url where a (supported) webapp is installed, the name of
        the web app, an optional number of files to check while guessing the
        version, and an optional logger object supporting the operations in 
        BlindElephantLogger (default is a FileLogger tied to sys.stdout)
        """
        self.url = url
        self.app_name = app_name
        self.num_probes = num_probes
        self.logger = logger
        self.winnow = winnow
        self._host_down_errors = 0
        self._error_page_fingerprint = None
    
    def _load_db(self):
        self.path_nodes, self.version_nodes, self.all_versions = \
            wadt.loadTables(wac.getDbPath(self.app_name), printStats=False)
        self.logger.logLoadDB(wac.getDbPath(self.app_name), self.all_versions, 
                              self.path_nodes, self.version_nodes)
    
    def fingerprint(self):
        """Select num_probes most useful paths, and fetch them
        from the site at url. Return an ordered list of possible versions or 
        [].
        """
        self._load_db()
        paths = wafu.pick_fingerprint_files(self.path_nodes, self.all_versions)
        self.logger.logStartFingerprint(self.url, self.app_name)
        
        self.error_page_fingerprint = wafu.identify_error_page(self.url)
        
        possible_vers = []
        for path in paths[:self.num_probes]:
            curr_vers = self.fingerprint_file(path)
            if curr_vers:
                possible_vers.append(curr_vers)
            if self._host_down_errors >= HOST_DOWN_THRESHOLD:
                break
        
        ver_set = wafu.collapse_version_possibilities(possible_vers)
        self.ver_list = list(ver_set)
        
        #if more than one possibility, try to narrow it by winnowing!
        if len(self.ver_list) > 1 and self.winnow:
            print "ver_list before winnowing:"
            for v in self.ver_list:
                print v.vstring
            print "\n"            
            self.winnow_versions(possible_vers)
        
        ver_set = wafu.collapse_version_possibilities(possible_vers)
        self.ver_list = list(ver_set)
        self.ver_list.sort()
        if len(self.ver_list) > 1:
            self.best_guess = wafu.pick_likely_version(self.ver_list)
        elif len(self.ver_list) == 1:
            self.best_guess = self.ver_list[0]
        else:
            self.best_guess = None
        self.logger.logFinishFingerprint(self.ver_list, self.best_guess)
        return self.ver_list
    
    def fingerprint_file(self, path):
        """Fingerprint a single file given the path, and return a list
        possible versions implied by the result, or None if no information
        could be gleaned.
        """
        try:
            url = self.url + (path if path.startswith("/") else "/"+path)
            data = wafu.urlread_spoof_ua(url)
            self._host_down_errors = 0
            hash = hashlib.md5(data + path).hexdigest()
            
            if self.path_nodes.has_key(hash):
                possible_vers = self.path_nodes[path][hash]
                self.logger.logFileHit(path, possible_vers, None, None, False)
                return possible_vers
            else:
                #HACKHACK TODO: Implement proper solution to small modifications of
                #source files
                ms = wafm.MASSAGERS
                
                #run all combinations of massagers to see if they can change the 
                #remote file into something we expect
                for i in range(1, len(ms)+1):
                    for massagersTpl in itertools.combinations(ms, i):
                        massagedData = data
                        for m in massagersTpl:
                            massagedData = m(massagedData)
                        massagedhash = hashlib.md5(massagedData + path).hexdigest()
                        if self.path_nodes[path].has_key(massagedhash):
                            possible_vers = self.path_nodes[path][massagedhash]
                            self.logger.logFileHit(path, possible_vers, "", None, False) #TODO: log massager use
                            return possible_vers
                
                #massagers turned up nothing, maybe it's a custom 404 page
                if wafu.compare_to_error_page(self.error_page_fingerprint, data):
                    self.logger.logFileHit(path, None, None, 'Detected Custom 404', True)
                    return None
                #give up and throw KeyError afterall
                possible_vers = self.path_nodes[path][hash]
                
        except IOError, e:
            if hasattr(e, 'reason'):
                self.logger.logFileHit(path, None, None, 
                    "Failed to reach a server: %s" % e.reason, True)
                self._host_down_errors += 1
            elif hasattr(e, 'code'):
                self.logger.logFileHit(path, None, None, 
                    'Error code: %s (%s)' % (e.code, BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]), 
                    True)
        except HTTPException, e2:
            self.logger.logFileHit(path, None, None, 'Error: %s ' % e2, True)
        except KeyError, e2:
            self.logger.logFileHit(path, None, None, 
                "Retrieved file doesn't match known fingerprint. %s" % e2.args, 
                True)
            
        return None
    
    def winnow_versions(self, possible_vers):
        winnow_attempts = 0
        while len(self.ver_list) > 1 and winnow_attempts < self.num_probes:
            winnow_paths = wafu.pick_winnow_files(self.ver_list, self.version_nodes, self.num_probes - winnow_attempts)
            if not winnow_paths:
                break
            for path in winnow_paths:
                winnow_attempts += 1
                curr_vers = self.fingerprint_file(path)
                if curr_vers:
                    possible_vers.append(curr_vers)
                    tmp_ver_set = wafu.collapse_version_possibilities(possible_vers)
                    #if winnowing knocked out a possibility, repick winnow files base on this new info
                    if len(tmp_ver_set) < len(self.ver_list):
                        self.ver_list = list(tmp_ver_set)
                        print "winnow eliminated a version... repicking"
                        continue
                if self._host_down_errors >= HOST_DOWN_THRESHOLD:
                    break
                if winnow_attempts > self.num_probes:
                    break
                



class PluginFingerprinter(WebAppFingerprinter):
    """Fingerprint the plugins of a particular webapp, using the same approach
    as WebAppFingerprinter. (Will find the plugins installation directory
    of configured apps automatically) 
    """
    
    #TODO: Revisit logging to differentiate plugin fingerprint output from app fingerprint output 
    def __init__(self, url, app_name, plugin_name, num_probes=15, logger=FileLogger(), winnow=False):
        """Same params as WebAppFingerprinter plus the name of plugin to 
        fingerprint. 
        """
        if not wac.APP_CONFIG[app_name].has_key("pluginsRoot"):
            raise NotImplementedError("Couldn't find pluginsRoot entry for %s in WebAppConfiguration. Plugins may not be supported for this app" % app_name)
        self.plugin_name = plugin_name
        super(PluginFingerprinter, self).__init__(url + wac.APP_CONFIG[app_name]["pluginsRoot"]+plugin_name, app_name, num_probes=num_probes)
        #super doesn't take keyword args; this is getting more and more annoying
        self.num_probes = num_probes
        self.logger = logger
        self.winnow = winnow
    
    def _load_db(self):
        #version_nodes is temporarily unused
        self.path_nodes, self.version_nodes, self.all_versions = \
            wadt.loadTables(wac.getDbPath(self.app_name, self.plugin_name), printStats=False)

class WebAppGuesser(object):
    
    def __init__(self, url, logger=FileLogger(wac.DEFAULT_LOGFILE)):
        self.url = url
        self.logger = logger
        self.error_page_fingerprint = None
        self.already_checked_for_error_page = False
        self._host_down_errors = 0

    def guess_apps(self, app_list=None):
        """Probe a small number of indicator files for each supported webapp to 
        quickly check for existence, but not version.
        """
        possible_apps = []
        if not self.error_page_fingerprint and not self.already_checked_for_error_page:
            self.error_page_fingerprint = wafu.identify_error_page(self.url)
            self.already_checked_for_error_page = True

        if not app_list:
            app_list = wac.APP_CONFIG.keys()
        
        for app in app_list:
            if self.guess_app(app):
                possible_apps.append(app)
            if self._host_down_errors >= HOST_DOWN_THRESHOLD:
                break
        return possible_apps
    
    def guess_app(self, app_name):
        """Probe a small number of paths to verify the existence (but not the 
        version) of a particular app
        """
        if not self.error_page_fingerprint and not self.already_checked_for_error_page:
            print "WARN: Fetching error page because it was not available"
            self.error_page_fingerprint = wafu.identify_error_page(self.url)
            self.already_checked_for_error_page = True

        path_nodes, version_nodes, all_versions = wadt.loadTables(wac.getDbPath(app_name), printStats=False)
        
        for file in wac.APP_CONFIG[app_name]["indicatorFiles"]:
            possible_vers = self.fingerprint_file(file, path_nodes, version_nodes, all_versions)
            if possible_vers:
                return True         
        return False
    
    def fingerprint_file(self, path, path_nodes, version_nodes, all_versions):
        """Fingerprint a single file given the path, and return a list
        possible versions implied by the result, or None if no information
        could be gleaned.
        """
        try:
            url = self.url + (path if path.startswith("/") else "/"+path)
            data = wafu.urlread_spoof_ua(url)
            self._host_down_errors = 0
            hash = hashlib.md5(data + path).hexdigest()
            
            if path_nodes.has_key(hash):
                possible_vers = path_nodes[path][hash]
                self.logger.logFileHit(path, possible_vers, None, None, False)
                return possible_vers
            else:
                #HACKHACK TODO: Implement proper solution to small modifications of
                #source files
                ms = wafm.MASSAGERS
                
                #run all combinations of massagers to see if they can change the 
                #remote file into something we expect
                for i in range(1, len(ms)+1):
                    for massagersTpl in itertools.combinations(ms, i):
                        massagedData = data
                        for m in massagersTpl:
                            massagedData = m(massagedData)
                        massagedhash = hashlib.md5(massagedData + path).hexdigest()
                        if path_nodes[path].has_key(massagedhash):
                            possible_vers = path_nodes[path][massagedhash]
                            return possible_vers
                
                #massagers turned up nothing, maybe it's a custom 404 page
                if wafu.compare_to_error_page(self.error_page_fingerprint, data):
                    return None
                #give up and throw KeyError afterall
                possible_vers = path_nodes[path][hash]
                
        except IOError, e:
            if hasattr(e, 'reason'):
                self._host_down_errors += 1
        except HTTPException, e2:
            pass
        except KeyError, e2:
            pass
        
        return None
    

class PluginGuesser(object):
    """Class that uses a BlindElephant fingerprint db to discover if a plugin or
    are installed in a web app.
    """

    def __init__(self, url, app_name, logger=FileLogger()):
        """Url should be the base url for the app (finding the plugin 
        directory is handled internally). App_name is required; it
        doesn't make sense to look for plugins if the app is unknown. 
        """
        self.app_name = app_name
        self.url = url + wac.APP_CONFIG[app_name]["pluginsRoot"]
        self.logger = logger

    def guess_plugin(self, plugin_name):
        """Check for the existence of the named plugin"""
        path_nodes, version_nodes, all_versions = \
            wadt.loadTables(wac.getDbPath(self.app_name, plugin_name), False)
        self.error_page_fingerprint = wafu.identify_error_page(self.url)
        
        for file in wafu.pick_indicator_files(version_nodes, all_versions):
            try:
                #TODO: factor out construction of path to plugin files... 
                #not all plugin dirs can be found simple appending
                url = self.url + plugin_name + file
                #self.logger.logExtraInfo("    Trying " + url + "...")
                data = wafu.urlread_spoof_ua(url)
                #Check for custom 404
                if wafu.compare_to_error_page(self.error_page_fingerprint, data):
                    return False                
                #self.logger.logExtraInfo("found!")
                return True
                break
            except urllib2.URLError, e:
                #self.logger.logExtraInfo("URLError: %s" % e)
                pass
            except HTTPException, e2:
                #self.logger.logExtraInfo("HTTPError: %s" % e2)
                pass
        return False
    
    def guess_plugins(self):
        """For the given app, check for the existence any known plugins, and
        return a list possible plugins. Obviously if the named app doesn't 
        exist, plugins probably won't exist""" 
        possible_plugins = []
        pluginsdir = wac.getDbDir(self.app_name)
        
        if os.access(pluginsdir, os.F_OK):    
            for plugin_name in filter(lambda x: x.endswith(wac.DB_EXTENSION), 
                                 sorted(os.listdir(pluginsdir))):
                plugin_name = plugin_name[:-(len(wac.DB_EXTENSION))] #trim DB_EXTENSION
                if self.guess_plugin(plugin_name):
                    possible_plugins.append(plugin_name)
        possible_plugins.sort()
        self.logger.logExtraInfo("Possible plugins: %s" % possible_plugins)
        return possible_plugins

