import urllib2
import BaseHTTPServer
from httplib import HTTPException 
from distutils.version import LooseVersion
import socket
import re
import operator


#TODO:
# - Unit tests for everything in this module

#How close a page needs to be to the reference error page in order to be considered a custom error page
#Range (0,1], with 1 being "exact match" between fingerprinted values 
ERROR_PAGE_SIMILARITY_TOLERANCE = .9

TIMEOUT = 5
socket.setdefaulttimeout(TIMEOUT)

def fingerprint_error_page(page_data):
    """Takes page_data as a string and returns an "error page fingerprint".
    (This error page "fingerprint" is different than the hash-based fingerprints
    used in the rest of BlindElephant.)
     
    (Implementation detail: It's a list (one entry per page type) containing dicts of tags that we care about and their counts)
    """
    error_page_fingerprint = {"</div>" : 0,
                              "</a>" : 0,
                              "</tr>" : 0,
                              "</p>": 0
                             }
    
    for tag in error_page_fingerprint:
        count = page_data.count(tag)
        count += page_data.count(tag.upper())
        error_page_fingerprint[tag] = count
    
    return error_page_fingerprint

def identify_error_page(base_url):
    """Fetches pages that should not exist on the host and looks for 
    characteristics that would help us identify custom error pages (HTTP 200 w/ 
    error text instead of 404).
    
    If not identified, custom error pages can be mistaken for 
    present-but-no-match hashes and screw up guessing and fingerprinting.
    
    Returns an "error page fingerprint" that can be passed to compare_to_error_page()
    See fingerprint_error_page()
    """
    retry = 2
    while retry:
        try:
            error_page_fingerprint = []
            
            #Various servers give different responses for non-existent text and graphics, so grab fingerprints for both
            url = base_url + "/should/not/exist.html" 
            data = urlread_spoof_ua(url)
            error_page_fingerprint.append(fingerprint_error_page(data))
            
            url = base_url + "/should/not/exist.gif"
            data = urlread_spoof_ua(url)
            error_page_fingerprint.append(fingerprint_error_page(data))

            #print "error page fingerprint:", error_page_fingerprint
            return error_page_fingerprint
        except IOError, e:
            if hasattr(e, 'code'):
                #if we got an error code back, that's all we need to know:
                #it doesn't use a custom 404
                return None
            else:
                retry -= 1
        except HTTPException, e2:
            #might be an httplib exception instead; eg BadStatusLine
            retry -= 1
    return None

def compare_to_error_page(error_page_fingerprint, page_data):
    """Check a page returned from a server against an error_page_fingerprint and 
    return True if the page is probably a custom error page, or False if not. 
    
    See identify_error_page()
    """
    #print "Checking page against error page"
    if not error_page_fingerprint:
        #print "Returning false because of no error page fingerprint"
        return False
    
    candidate_fingerprint = fingerprint_error_page(page_data)
    #print "Error page fingerprint:", error_page_fingerprint
    #print "Candidate fingerprint:", candidate_fingerprint
    #Parked domains respond with random stuff; doing manual exceptions for now until a pattern emerges
    parking_phrases = ["GoDaddy.com is the world's No. 1 ICANN-accredited domain name registrar", "This site is not currently available."]
    for phrase in parking_phrases:
        if phrase in page_data:
            #print "Identified custom 404 because of phrase:", phrase
            return True 
    
    for pagetype in error_page_fingerprint:
        for tag in pagetype:
            tag_count_diff = abs(pagetype[tag] - candidate_fingerprint[tag])
            bigger_count = max(pagetype[tag], candidate_fingerprint[tag])
            tolerance =  (bigger_count - (bigger_count * ERROR_PAGE_SIMILARITY_TOLERANCE))
            #print "Tag: %s\tErrPg: %d\tCandidate: %d" % (tag, error_page_fingerprint[tag], candidate_fingerprint[tag])
            #if a single value exceeds tolerance, we're done
            if tag_count_diff > tolerance:
                return False
    return True

def collapse_version_possibilities(possible_vers):
    """Take a list of version lists and return the intersection set or [] if 
    it's empty
    """
    ver_sets = [set(v) for v in filter(None,possible_vers)]
    try:
        ver_set = reduce(lambda a, b: a & b, ver_sets)
    except:
        ver_set = []
    
    if possible_vers and not ver_set:
        ver_set = resolve_conflicting_data(possible_vers) 
    return ver_set

def get_version_map(ver_list):
    """Uses possible versions resulting from a fingerprint attempt and returns a dict that maps degenerate 
    versions their corresponding primary/strict version (if one was present in ver_list)
    or to itself otherwise (it won't make up versions that don't already exist).
    Eg:
        get_version_map([LooseVersion("1.3.4"), LooseVersion("1.3.4-RC2"), LooseVersion("1.3.5-beta1")])
        -> {LooseVersion("1.2.3-RC2") : LooseVersion("1.2.3"), 
            LooseVersion("1.3.5-beta1") : LooseVersion("1.3.5-beta1")}
    
    Useful for imposing a rough but consistent ordering or simplifying output
    """
    mapping = {}
    for ver in ver_list:
        #extract the strict part
        match = re.match("([\d.]+)", ver.vstring)
        #print "match.groups():", match.groups()
        if match and match.group(0) and match.group(0) != ver:
            tover = LooseVersion(match.group(0))
            if tover in ver_list:
                #print "Mapping %s to %s" % (ver, tover)
                mapping[ver] = tover
            else:
                #print "Mapping %s to %s (self)" % (ver, tover)
                mapping[ver] = ver
        else:
            #print "%s does not need mapping" % ver
            mapping[ver] = ver
    #print "Map:", mapping
    return mapping

def resolve_conflicting_data(possible_vers):
    """Takes a list of lists of vers and considers only the smallest list as valid data; returns that list.
    (There are of course other reasonable ways to resolve the conflict; this one was expedient.)
    """
    smallest = None
    for vers in possible_vers:
        if not smallest or len(vers) < len(smallest):
            smallest = vers
    return smallest

def pick_likely_version(ver_list):
    """Using possible versions from a fingerprint attempt, attempt to pick the latest. 
    See get_version_map
    """
    if not ver_list:
        return None
    vermap = get_version_map(ver_list)
    simplified_ver_list = [vermap[ver] for ver in ver_list]
    simplified_ver_list.sort()
    return simplified_ver_list[-1]

def pick_fingerprint_files(path_nodes, all_versions):
    """Examine all known paths and return a list (of all paths) ordered by 
    their ability to give us lots of information about the install.
    This is important since we only want to fetch paths that are present in 
    lots of versions, *and* we want there to be a lot of changes in the hash
    between versions
    
    This uses a fitness function that can be tweaked over time; right now 
    it's just a rough "best guess" about the value of fetching each path... 
        
    Future work is to take into account the versions reported on and try to acheive
    set coverage with minimal files.
    
    Returns an ordered list of paths.
    """
    #find a path with the best fitness
    candidate_nodes = []
    
    for path in path_nodes.keys():
        currvers = []
        currhashes = len(path_nodes[path])
        
        for hash in path_nodes[path]:
            currvers.extend(path_nodes[path][hash])
        
        fitness = ( float(len(currvers))/float(len(all_versions)) )+currhashes
        candidate_nodes.append({"fitness": fitness, "path" : path})
    
    candidate_nodes.sort(key=operator.itemgetter('fitness'), reverse=True)
    return [f["path"] for f in candidate_nodes]

def pick_indicator_files(version_nodes, all_versions):
    """Choose a small number of files that (should) reliably indicate
    whether an app or plugin exists. Returns an ordered list of paths.""" 
    #TODO: this whole method is kindof fuzzy/best guess and ends up returning
    #some plugins w/ 2 files and others with 6. Could be more effecient 
    #and predictable, but it's generic and does the job for now.    
    nodes = []
    threshold = len(all_versions)
    
    # If we can find a version node that represents every possible version for
    # the app/plugin we're looking at (aka contains a file that is present in 
    # every known version) then that's the ideal choice, so start with that: 
    # threshold = len(allversions).
    # Realistically there won't be a single file that accomplishes that, so we
    # lower the threshold until we find at least two different groups of 
    # files. That seems to be the sweet spot. TODO: More testing on that.
    while len(nodes) < 2 and threshold > 0:
        #try some numbers close to the total number of versions, backing off 
        #until vers isn't empty
        nodes = filter(lambda k: len(k.split(",")) >= threshold, version_nodes.keys()) 
        threshold -= 1;

    indicator_files = []
    for ver in nodes:
        for n in version_nodes[ver][:2]:
            indicator_files.append(n[0])
    return list(set(indicator_files))


def urlread_spoof_ua(url):
    """I really hate to do this, but various spam, advertising and domain parking sites
    won't give either a 404 or a consistent landing page without pretending like we're a browser.
    """
    req = urllib2.Request(url, headers={"User-agent" : "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3"})
    data = urllib2.urlopen(req, timeout=TIMEOUT).read()
    return data

def pick_winnow_files(possible_ver_list, version_nodes, max_paths):
    """Given a condensed ver list (and version nodes), return paths (up to max_paths) 
    that may be able to rule out some of the versions.
    """
    #TODO: This is a not an efficient way of picking files, but it gives some improvement. 
    #Changes to the keying and contents of version_nodes are probably the best way to significantly improve winnowing
    winnow_paths = []
    selected_version_groups = []
    for ver in possible_ver_list:
        print "for ver: %s  len winnow_paths: %s    max_paths: %s" % (ver, len(winnow_paths), max_paths)
        for vergroup in version_nodes:
            #print "  for vergroup:", vergroup
            if ver.vstring in vergroup and len(vergroup.split(",")) < len(possible_ver_list) and vergroup not in selected_version_groups:
                winnow_paths.append(version_nodes[vergroup][0][0])
            if len(winnow_paths) >= max_paths:
                #print "returning winnow paths" 
                return winnow_paths
    #print "returning winnow paths 2"            
    return winnow_paths
