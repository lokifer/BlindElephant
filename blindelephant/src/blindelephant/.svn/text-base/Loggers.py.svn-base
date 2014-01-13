import sys


class FileLogger(object):
    def __init__(self, file=sys.stdout):
        self.file = file
    
    def logLoadDB(self, filename, all_versions, path_nodes, version_nodes):
        print >> self.file, "Loaded %s with %s versions, %s differentiating paths, and %s version groups." % (filename, len(all_versions), len(path_nodes), len(version_nodes))
  
    def logFileHit(self, path, versions, massagers, error, nomatch):
        print >> self.file, "Hit", self.url + path
        if nomatch:
            print >> self.file, "File produced no match. Error:", error, "\n"
        else:
            print >> self.file, "Possible versions based on result: %s\n" % (", ".join([v.vstring for v in sorted(versions)]))
    
    def logStartFingerprint(self, url, app_name):
        self.url = url
        self.app_name = app_name
        print >> self.file, "Starting BlindElephant fingerprint for version of", app_name, "at", url, "\n"
    
    def logFinishFingerprint(self, versions, best_guess):
        print >> self.file, ""
        if versions:
            print >> self.file, "Fingerprinting resulted in:"
            for ver in versions:
                print >> self.file, ver.vstring
            print >> self.file, "\n\nBest Guess:", best_guess.vstring
        else:
            print >> self.file, "Error: All versions ruled out!"
            
    def logExtraInfo(self, str):
        print >> self.file, str
