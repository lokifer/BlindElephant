
ADDING NEW WEB APPLICATIONS TO BLIND ELEPHANT.
-----------------------------------------------------
Currently supported apps and plugins can be listed with ./BlindElephant.py -l

If an app you're interested in isn't supported please consider diving in and making it happen. With most apps it should take only an hour or so.

I use some simple scripts to fetch new versions of all supported apps nightly, but won't be releasing them since we don't need a thousand people abusing the various mirrors. Contact me (pst@coffeetocode.net) if you wish to support a new app and I'll see if I can save you some time. If you choose to follow the conventions here I can probably add the app to the nightly build and save you a *lot* of time.

For the steps below I'll be using TWiki as example.



1) Add keys to the end of APP_CONFIG in Configuration.py


2) Create directory structure to hold all the app versions. I use ~/webAppSources (if you choose something different, change APPS_PATH in Configuration.py accordingly)
 cd ~/webAppSources
 mkdir twiki
 cd twiki
 mkdir downloads


3) Get all versions of the app you can find (say, TWiki-*.zip) and dump them in ~webAppSources/<appname>/downloads
(LatestVersionFetcher provides example functions that may help automate this. Otherwise there's always DownThemAll on Firefox ;)


4) Examine the file structure of the zips and create a bash script to unpack them. The goal is to have ~/webAppSources/<appname> be filled with dirs that contain easily extractable versions. Something like:

~/webAppSources/movabletype$ ls
downloads       MT-4.261-en        MTCS-4.05-en-CS   MTOS-4.25-en
movabletype.sh  MT-4.26-en         MTCS-4.121-en     MTOS-4.25-en-OS
MT-3.31         MT-4.2-en          MTCS-4.121-en-CS  MTOS-4.261-en
MT-3.32         MT-4.31-en         MTCS-4.131-en     MTOS-4.261-en-OS
MT-3.33         MT-4.32-en         MTCS-4.131-en-CS  MTOS-4.26-en
MT-3.34-en      MT-4.33-en         MTCS-4.141-en     MTOS-4.26-en-OS
... <etc>

Unpacker scripts live in tools/ (for version control purposes), but get copied into webAppSources/<appname>/ before invocation.
 cd webAppSources/twiki
 touch twiki.sh
 chmod +x
 (read twiki.sh or others for the general idea)


5) Run the unpacker script
 cd ~/webAppSources/twiki
 ./twiki.sh

5) Update APP_CONFIG key with any files or directories to exclude, eg  .php, .pl, bin/, install/ (see existing entries for formatting).


6) Update/create fingerprint datafiles
python LatestVersionFetcher.py --updateDBs twiki


7) Choose indicator files (this step is a holdover from a previous more manual method that we hope to get away from. In the future this will probably be done automatically at runtime unless overridden)
cd src/blindelephant/
python

import DifferencesTables as dt
import FingerprintUtils as fu
import Configuration as c
pathNodes, versionNodes, allVersions = dt.loadTables(c.getDbPath("twiki"), printStats=True, useCaching=False)
fu.pick_indicator_files(versionNodes, allVersions)
['/pub/TWiki/TWikiDocGraphics/sitemap.gif', '/pub/TWiki/TinyMCEPlugin/tinymce/docs/index.html', '/COPYING', '/pub/TWiki/JSCalendarContrib/lang/calendar-fi.js', '/pub/TWiki/TWikiDocGraphics/mail.gif', '/LICENSE']
Paste the result into the indicatorFiles key of the webapp config entry.

8) Try it out!
python BlindElephant.py http://example.com/twiki/ twiki
