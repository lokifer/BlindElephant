BlindElephant Web Application Fingerprinter

I.   SUMMARY
II.  PREREQUISITES
III. INSTALLATION
IV.  EXAMPLE USAGE (command line)
V.   EXAMPLE USAGE (library)

I. SUMMARY:
-----------------------------------------------------------------
The BlindElephant Web Application Fingerprinter attempts to discover the version
of a (known) web application by comparing static files at known locations against
precomputed hashes for versions of those files in all all available releases. 

The technique is fast, low-bandwidth, non-invasive, generic, and highly automatable. 

Author: Patrick Thomas (pthomas@qualys.com, pst@coffeetocode.net)

Sites: https://sourceforge.net/projects/blindelephant/
       http://www.qualys.com/blindelephant

II. PREREQUISITES:
-----------------------------------------------------------------
Python == 2.6.x (greater than 2.6.x may work, less than probably will not; neither is tested)


III. INSTALLATION (via distutils):
-----------------------------------------------------------------
python setup.py install


IV. EXAMPLE USAGE (command line):
-----------------------------------------------------------------
$ python BlindElephant.py 
Error: url and appName are required arguments unless using -l, -u, or -h

Usage: BlindElephant.py [options] url appName

Options:
  -h, --help            show this help message and exit
  -p PLUGINNAME, --pluginName=PLUGINNAME
                        Fingerprint version of plugin (should apply to web app
                        given in appname)
  -s, --skip            Skip fingerprinting webpp, just fingerprint plugin
  -n NUMPROBES, --numProbes=NUMPROBES
                        Number of files to fetch (more may increase accuracy).
                        Default: 15
  -w, --winnow          If more than one version are returned, use winnowing
                        to attempt to narrow it down (up to numProbes
                        additional requests).
  -l, --list            List supported webapps and plugins

Use "guess" as app or plugin name to attempt to attempt to
discover which supported apps/plugins are installed.

$ python BlindElephant.py http://laws.qualys.com movabletype
Loaded /usr/local/lib/python2.6/dist-packages/blindelephant/dbs/movabletype.pkl with 96 versions, 2229 differentiating paths, and 209 version groups.
Starting BlindElephant fingerprint for version of movabletype at http://laws.qualys.com 

Hit http://laws.qualys.com/mt-static/mt.js
Possible versions based on result: 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/client.js
Possible versions based on result: 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/css/main.css
Possible versions based on result: 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM

Hit http://laws.qualys.com/tools/run-periodic-tasks
File produced no match. Error: Error code: 404 (Not Found) 

Hit http://laws.qualys.com/mt-static/js/tc/tagcomplete.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/edit.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/mixer/display.js
Possible versions based on result: 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/archetype_editor.js
Possible versions based on result: 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/mixer.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/tableselect.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/focus.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/css/simple.css
Possible versions based on result: 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM

Hit http://laws.qualys.com/mt-static/mt_ja.js
Possible versions based on result: 4.2-en, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.23-en-OS, 4.24-en, 4.24-en, 4.24-en-COM

Hit http://laws.qualys.com/mt-static/js/tc/gestalt.js
Possible versions based on result: 4.1-en, 4.1-en-CS, 4.2-en, 4.21-en, 4.21-en, 4.21-en-COM, 4.22-en, 4.22-en, 4.22-en-COM, 4.23-en, 4.23-en, 4.23-en-COM, 4.24-en, 4.24-en, 4.24-en-COM


Fingerprinting resulted in:
4.22-en
4.22-en-COM
4.23-en
4.23-en-COM


Best Guess: 4.23-en-COM


V. EXAMPLE USAGE (as library):
-----------------------------------------------------------------
$python
>>> from blindelephant.Fingerprinters import WebAppFingerprinter
>>> 
>>> #Construct the fingerprinter
>>> #use default logger pointing to console; can pass "logger" arg to change output
>>> fp = WebAppFingerprinter("http://laws.qualys.com", "movabletype")
>>> #do the fingerprint; data becomes available as instance vars
>>> fp.fingerprint()
<snip>(same as above)</snip>
>>> print "Possible versions:", fp.ver_list
Possible versions: [LooseVersion ('4.22-en'), LooseVersion ('4.22-en-COM'), LooseVersion ('4.23-en'), LooseVersion ('4.23-en-COM')]
>>> print "Max possible version: ", fp.best_guess
Max possible version:  4.23-en-COM
