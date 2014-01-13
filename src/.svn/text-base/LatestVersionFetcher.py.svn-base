import blindelephant.DifferencesTables as dt
import blindelephant.Configuration as config
import re
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser
import urllib2
import time
import urllib
import os

#====================================================
#This file grabs the latest releases of supported webapps and copies them to the downloads dir of each webapp 
#It should usually be run via cron job
#====================================================

#TODO:
# - Refactor to do away with the idea of the strainer; just call fetcher with a list of filename and dl locations
# - Sometimes zips come down empty (eg latest version of some wordpress plugins) -- detect and reject these bogus new versions

#the soup strainer here isn't exactly what's described in the BeautifulSoup documentation
#soupStrainerFunc is expected to consume a beautifulSoup object and produce a list of {'href': ..., 'filename': ...} objects
#representing all the currently available versions... some strainers load additional pages in order to collect links (eg, mediawiki)
#downloads prefix should be provided if strained links are relative, can be omitted if absolute
def _fetchTemplate(appName, releasesUrl, soupStrainerFunc, downloadsPrefix="", plugin=None):
    knownFiles = os.listdir(config.APPS_PATH + appName + ("-plugins/"+plugin if plugin else "") + "/downloads")

    #print "Known:" 
    #for file in sorted(knownFiles):
    #    print file
    #print "Fetching: ", releasesUrl
    f = urllib2.urlopen(releasesUrl)
    soup = BeautifulSoup(f.read())
    f.close()
    
    availableFiles = soupStrainerFunc(soup)
    #print "Available files:"
    #for f in availableFiles:
    #    print f

    newVersTemp = [f for f in availableFiles if f['filename'] not in knownFiles]
    
    #Some sites, notably sourceforge, offer the same download url twice. 
    #Uniqify list so as not to re-download a file twice in one session
    #(just converting to set() won't work... dicts aren't hashable)
    newVers = []
    for v in newVersTemp:
        if v not in newVers:
            newVers.append(v)

    #print "New files:"
    #for f in availableFiles:
    #    print f
    
    for v in sorted(newVers):
        #throttle to not abuse remote server
        time.sleep(1.5)
        #TODO: add a check that we're not re
        print "Attempting to fetch:", downloadsPrefix + v['href']
        
        #create the url and the request 
        url = downloadsPrefix + v['href']
        req = urllib2.Request(url)
        
        # Open the url
        try:
            f = urllib2.urlopen(req)
            # Open our local file for writing
            local_file_path = config.APPS_PATH + appName + ("-plugins/"+plugin if plugin else "") + "/downloads/"+v['filename']
            #print "Writing", local_file_path
            local_file = open(local_file_path, "wb")
            #Write to our local file
            local_file.write(f.read())
            local_file.close()
    
        #handle errors
        except urllib2.HTTPError, e:
            print "HTTP Error:",e.code , url
        except urllib2.URLError, e:
            print "URL Error:",e.reason , url
            
    return [v['filename'] for v in newVers]


#Fetchers for currently supported apps not being released right now, sorry; I don't want to make it easy to abuse the mirrors. 
#Contact me if you need them for some reason.

#example fetchers for new apps
def _exampleStrainer(soup):
    links = soup.findAll('a', attrs={'href' : lambda s: s and s.endswith('.tar.gz')})
    
    availableFiles = []
    for link in links:        
        availableFiles.append({'href' : link['href'], 'filename' : link.string})
    return availableFiles

def fetchexample():
    return _fetchTemplate('appname', "http://example.com/releases", _exampleStrainer, "")



def updateDbs(apps):
    """Used to create .pkl files for any apps or plugins the are declared 
    supported but don't have an up-to-date pkl file. 
    Takes a list of appnames.
    """
    for app in apps:
        if not os.access(config.getDbPath(app), os.F_OK):
            print "No db file available for app %s. Creating it from %s..." % (app, config.getAppPath(app))
            pathNodes, versionNodes, allversions = dt.computeTables(config.getAppPath(app), config.APP_CONFIG[app]["versionDirectoryRegex"], config.APP_CONFIG[app]["directoryExcludeRegex"], config.APP_CONFIG[app]["fileExcludeRegex"])
            dt.saveTables(config.getDbPath(app), pathNodes, versionNodes, allversions)
        else:
            print "Found db file for app %s" % app,
            #print "(path is ", config.getDbPath(app), ")"
            pathNodes, versionNodes, allversions = dt.loadTables(config.getDbPath(app), False)
            versInDb = len(allversions)
            versOnDisk = len(filter(lambda entry: re.match(config.APP_CONFIG[app]["versionDirectoryRegex"], entry),os.listdir(config.getAppPath(app))))

            #versInDb = set(ver.vstring for ver in allversions)
            #versOnDisk = set([entry for entry in os.listdir(config.getAppPath(app)) if re.match(config.APP_CONFIG[app]["versionDirectoryRegex"], entry)])
            #verDifferences = versInDb ^ versOnDisk
            #print "DB: %s\nDisk: %s\nDiffs: %s" % (versInDb, versOnDisk, verDifferences)
            if versInDb != versOnDisk:
                print "but it is out of date (%s versions in db, %s versions on disk). Recreating it from %s... " % (versInDb, versOnDisk, config.getAppPath(app))
                pathNodes, versionNodes, allversions = dt.computeTables(config.getAppPath(app), config.APP_CONFIG[app]["versionDirectoryRegex"], config.APP_CONFIG[app]["directoryExcludeRegex"], config.APP_CONFIG[app]["fileExcludeRegex"])
                dt.saveTables(config.getDbPath(app), pathNodes, versionNodes, allversions)
            else:
                print "."
        
        if os.access(config.getAppPluginPath(app), os.F_OK):
            for plugin in filter(lambda p: os.path.isdir(config.getAppPluginPath(app, p)), sorted(os.listdir(config.getAppPluginPath(app)))):
                if not os.access(config.getDbPath(app, plugin), os.F_OK):
                    print "No db file available for %s plugin %s. Creating it from %s..." % (app, plugin, config.getAppPluginPath(app, plugin))
                    pathNodes, versionNodes, allversions = dt.computeTables(config.getAppPluginPath(app, plugin),  plugin+config.APP_CONFIG[app]["pluginsDirectoryRegex"], "none", config.APP_CONFIG[app]["fileExcludeRegex"])
                    dt.saveTables(config.getDbPath(app, plugin), pathNodes, versionNodes, allversions)
                else:
                    print "Found db file for %s plugin %s" % (app, plugin),
                    pathNodes, versionNodes, allversions = dt.loadTables(config.getDbPath(app, plugin), False)                    
                    versInDb = len(allversions)
                    versOnDisk = len(filter(lambda entry: re.match(plugin+config.APP_CONFIG[app]["pluginsDirectoryRegex"], entry),os.listdir(config.getAppPluginPath(app, plugin))))
                    if versInDb != versOnDisk:
                        print "but it is out of date (%s versions in db, %s versions on disk). Recreating it from %s... " % (versInDb, versOnDisk, config.getAppPluginPath(app, plugin))
                        pathNodes, versionNodes, allversions = dt.computeTables(config.getAppPluginPath(app, plugin), plugin+config.APP_CONFIG[app]["pluginsDirectoryRegex"], config.APP_CONFIG[app]["directoryExcludeRegex"], config.APP_CONFIG[app]["fileExcludeRegex"])
                        dt.saveTables(config.getDbPath(app, plugin), pathNodes, versionNodes, allversions)
                    else:
                        print "."
                    



if __name__ == '__main__':
 
    USAGE = "usage: %prog [options] appName"
    EPILOGUE = "Download newly-available releases of supported WebApplications.\nUse \"all\" as an app name to update all known." 
    
    parser = OptionParser(usage=USAGE, epilog=EPILOGUE)
    parser.add_option("-p", "--plugins", action="store_true", help="Fetch all plugins for the given app")
    parser.add_option("-u", "--updateDBs", action="store_true", help="Update databases (developer use only)")
    
 
    (options, args) = parser.parse_args()

    if options.updateDBs:
       if len(args) < 1 or args[0] == "all":
           args = [app for app in config.APP_CONFIG.keys()]
       print args
       updateDbs(args)
       quit()
    
    if len(args) < 1:
        print "Error: AppName is required\n"
        parser.print_help()
        quit()
 
    if args[0] == "all":
        for func in filter(lambda s: s.startswith("fetch"),sorted(globals().keys())):
            print func
            time.sleep(2)
            print globals()[func]()
    elif globals().has_key("fetch"+args[0]):
        print "Checking for new versions of", args[0]
        print globals()["fetch"+args[0]]()
        if options.plugins:
            print "Checking for new versions of", args[0], "plugins"
            eval("fetch"+args[0]+"plugins()")

    else:
        print "Error: "+args[0]+" is not supported for fetching latest versions (do it manually or add it here)\n"
        parser.print_help()
        quit()
 
