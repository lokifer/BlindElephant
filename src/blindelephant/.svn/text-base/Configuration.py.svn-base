"""Common configuration information for all BlindElephant code"""
import os
import sys

#Wherever this Configuration module lives, the the default dbs folder should be
#there too, so load it relative to the dir this module was loaded from. 
DBS_PATH = os.path.join(os.path.dirname(__file__), "dbs/")

#The DB extension was originally ".db"; references to "database files" or "db files"
#can be assumed to refer to the files with .pkl extensions.  
DB_EXTENSION = ".pkl"
PLUGINS_EXTENSION = "-plugins"

#include trailing '/' please
APPS_PATH = os.path.expanduser("~/webAppSources/")

DEFAULT_LOGFILE = sys.stdout

#===============================================================================
#To regenerate the .pkl files, make sure that APPS_PATH below points to a 
#directory containing a folder named for each supported webapp, and inside that 
#are app-root folders named for the version they contain 
#
#Plugins (if any) should live at "[appname]-plugins"
#
#If you need to get copies, they're all at smb://10.10.27.4/store/webApps as 
#both compressed files (as downloaded) and unpacked, consistently named 
#directories suitable for parsing. 
#
# Additional apps (some not yet supported) are at 10.10.30.205
#
# eg:
# pthomas@patrick-desktop:~/webAppSources$ ls -R
# .:
# drupal          mediawiki    oscommerce        phpnuke   wordpress
# drupal-plugins  joomla       moodle            phpbb     liferay  
# movabletype     phpmyadmin   wordpress-plugins
# 
# ./drupal:
# downloads      drupal-4.6.6        drupal-5.0-beta2  drupal-6.0-beta2
# drupal-4.0.0   drupal-4.6.7        drupal-5.0-rc1    drupal-6.0-beta3
# drupal-4.1.0   drupal-4.6.8        drupal-5.0-rc2    drupal-6.0-beta4
# drupal-4.2.0   drupal-4.6.9        drupal-5.1        drupal-6.0-rc1
# drupal-4.3.0   drupal-4.6.x-dev    drupal-5.10       drupal-6.0-rc2
# <snip>
# 
# ./drupal/downloads:
# drupal-4.0.0.tar.gz        drupal-4.7.0-rc2.tar.gz  drupal-5.5.tar.gz
# drupal-4.1.0.tar.gz        drupal-4.7.0-rc3.tar.gz  drupal-5.6.tar.gz
# drupal-4.2.0.tar.gz        drupal-4.7.0-rc4.tar.gz  drupal-5.7.tar.gz
# drupal-4.3.0.tar.gz        drupal-4.7.0.tar.gz      drupal-5.8.tar.gz
# drupal-4.3.1.tar.gz        drupal-4.7.10.tar.gz     drupal-5.9.tar.gz
# drupal-4.3.2.tar.gz        drupal-4.7.11.tar.gz     drupal-5.x-dev.tar.gz
# drupal-4.4.0.tar.gz        drupal-4.7.1.tar.gz      drupal-5.x-dev.tar.gz.stale
# drupal-4.4.1.tar.gz        drupal-4.7.2.tar.gz      drupal-6.0-beta1.tar.gz
# <snip>
# 
# ./drupal/drupal-4.0.0:
# admin.php  error.php    INSTALL      module.php  themes
# CHANGELOG  favicon.ico  LICENSE      modules     update.php
# cron.php   includes     MAINTAINERS  node.php    xmlrpc.php
# database   index.php    misc         scripts
#===============================================================================


#simplify code for finding .pkl files and dirs
def getDbPath(appName, pluginName=None):
    """Given appname (and optional plugin name), returns something like 
    dbs/drupal.pkl (or dbs/wordpress-plugins/stats.pkl).
    """
    return DBS_PATH + appName + ((PLUGINS_EXTENSION + "/" + pluginName) if pluginName else "") + ".pkl"

  
def getDbDir(appName=None):
    """Get the path of the app db directory, or an app plugin db directory if 
    optional appName is passed
    """
    return DBS_PATH + (appName + PLUGINS_EXTENSION + "/" if appName else "")

def getAppPath(appName):
    """Get the path to the sources directory for the named app. 
    Developer only - For use in rebuilding DBs.
    """
    return APPS_PATH + appName

def getAppPluginPath(appName, pluginName=None):
    """Get path to plugin dirs for an app (or with optional pluginName to a 
    specific plugin). 
    Developer Only - For use in rebuilding DBs.
    """
    return APPS_PATH + appName + PLUGINS_EXTENSION + "/" + (pluginName + "/" if pluginName else "") 

"""
Should have a key for every supported webapp. Indexed by that key should be a 
dict providing info creating and using the fingerprint db.
Each webapp dict should contain:
 - versionDirectoryRegex
 - directoryExcludeRegex
 - fileExcludeRegex
 - indicatorFiles
 
 Only if plugins are supported:
 - pluginsRoot
 - pluginsDirectoryRegex
 
Read WebAppDifferencesTables.computeTables or existing entries for specifics
"""
APP_CONFIG =   { "joomla" : {"versionDirectoryRegex" : "Joomla_([\d.]+).*",
                             "directoryExcludeRegex" : "installation|administrator",
                             "fileExcludeRegex": ".*\.(?:php|xml|php5|htaccess)$",
                             "indicatorFiles": ["/includes/js/dtree/img/frontpage.gif", "/images/banners/osmbanner2.png", "/media/system/js/mootools.js", "/images/joomla_logo_black.jpg", "/includes/js/wz_tooltip.js", "/includes/js/tabs/tabpane_mini.js"]
                             },
                 "mediawiki" : {"versionDirectoryRegex" : "mediawiki-(.*)",
                                "directoryExcludeRegex" : "installation|administrator|maintenance",
                                "fileExcludeRegex": ".*\.(?:php|xml|php5|htaccess)$",
                                "indicatorFiles": ["/docs/php-memcached/Documentation", "/math/mathml.mli", "/includes/zhtable/printutf8.c", "/skins/common/quickbar.css", "/skins/monobook/magnify-clip.png"]
                                },
                 "wordpress" : {"versionDirectoryRegex" : "wordpress-(.*)",
                                "directoryExcludeRegex" : "wp-admin",
                                "fileExcludeRegex": ".*\.(?:php|xml|php5|htaccess)$",
                                "indicatorFiles": ["/wp-includes/js/wp-lists.js", "/wp-content/plugins/akismet/akismet.gif", "/wp-content/themes/default/screenshot.png", "/wp-images/wpminilogo.png"],
                                "pluginsRoot": "/wp-content/plugins/",
                                "pluginsDirectoryRegex": "\.(.*)"
                                },
                 "phpbb" : {"versionDirectoryRegex" : "php[bB]{2}-(.*)",
                            "directoryExcludeRegex" : "none",
                            "fileExcludeRegex" : ".*\.(?:php|xml|php|htaccess)$",
                            "indicatorFiles" : ["/images/avatars/gallery/index.htm", "/adm/style/permission_trace.html", "/images/smilies/icon_e_confused.gif"]
                            },
                 "movabletype" : {"versionDirectoryRegex" : "MT[^-]*-(.*)",
                                  "directoryExcludeRegex" : "none",
                                  "fileExcludeRegex": ".*\.(?:php|xml|php5|pm|cgi|pl|tmpl|htaccess)$",
                                  "indicatorFiles" : ["/mt-static/images/spinner-big-bottom.gif", "/mt-static/images/status_icons/feed-disabled.gif", "/mt-static/plugins/WidgetManager/js/app.js"]
                                 },
                 "drupal" : {"versionDirectoryRegex" : "drupal-(.*)",
                             "directoryExcludeRegex" : "includes|modules",
                             "fileExcludeRegex": ".*\.(?:php|xml|php5|info|htaccess|theme|engine|pl)$",
                             "indicatorFiles" : ["/misc/drupal.js", "/themes/chameleon/marvin/bullet.png", "/themes/pushbutton/arrow-up-visited.png", "/misc/throbber.gif", "/misc/watchdog-error.png"],
                             "pluginsRoot": "/sites/all/modules/", #TODO: Also support /modules/
                             "pluginsDirectoryRegex": "-(.*)"
                            },
                 "oscommerce" : {"versionDirectoryRegex" : "oscommerce-(.*)",
                                 "directoryExcludeRegex" : "none",
                                 "fileExcludeRegex": ".*\.(?:php|xml|php5|info|htaccess|theme|engine|pl)$",
                                 "indicatorFiles" : ["/includes/local/README", "/images/table_background_password_forgotten.gif", "/images/table_background_address_book.gif"]
                                },
                 "phpnuke" : {"versionDirectoryRegex" : "PHP-Nuke-(.*)",
                              "directoryExcludeRegex" : "none",
                              "fileExcludeRegex": ".*\.(?:php|xml|php5|info|htaccess|theme|engine|pl)$",
                              "indicatorFiles" : ["/ultramode.txt", "/blocks/readme.txt", "/images/green_dot.gif", "/images/powered/nuke.gif"]
                            },
                 "moodle" : {"versionDirectoryRegex" : "moodle-(.*)",
                             "directoryExcludeRegex" : "none",
                             "fileExcludeRegex": ".*\.(?:php|php5|info|htaccess|theme|engine|pl)$",
                             "indicatorFiles" : ["/pix/s/clown.gif", "/lib/editor/tinymce/jscripts/tiny_mce/themes/simple/css/editor_ui.css", "/question/format/qti2/templates/textEntry.tpl", "/user/default/f2.jpg", "/mod/glossary/README.txt"]
                            },
                 "liferay" : {"versionDirectoryRegex" : "liferay-portal-(.*)",
                              "directoryExcludeRegex" : "none",
                              "fileExcludeRegex": ".*\.(?:jsp|htaccess)$",
                              "indicatorFiles" : ["/html/common/null.html", "/html/sound/mail/new_mail_1.wav", "/html/js/editor/fckeditor/editor/dialog/fck_spellerpages/spellerpages/controlWindow.js", "/html/themes/classic/images/liferay.ico"]
                             },
                 "phpmyadmin" : {"versionDirectoryRegex" : "phpMyAdmin-(.*)",
                                 "directoryExcludeRegex" : "libraries|scripts",
                                 "fileExcludeRegex": ".*\.(?:php|php3|htaccess)$",
                                 "indicatorFiles" : ["/Documentation.txt", "/images/fulltext.png", "/translators.html", "/scripts/remove_control_m.sh", "/lang/remove_message.sh"]
                                },
                 "spip" : {"versionDirectoryRegex" : "spip_(.*)",
                           "directoryExcludeRegex" : "none",
                           "fileExcludeRegex": ".*\.(?:php|php3|html)$",
                           "indicatorFiles" : ["/dist/ical.html", "/squelettes-dist/ical.html", "/ecrire/gpl_fr.txt"]
                           },
                 "twiki" : {"versionDirectoryRegex" : "TWiki-(.*)",
                           "directoryExcludeRegex" : "lib|bin|tools|templates|locale|data|foo",
                           "fileExcludeRegex": ".*\.(?:pm|pl|.sh)$",
                           "indicatorFiles" : ['/pub/TWiki/TWikiDocGraphics/sitemap.gif', '/pub/TWiki/TinyMCEPlugin/tinymce/docs/index.html', '/COPYING', '/pub/TWiki/JSCalendarContrib/lang/calendar-fi.js', '/pub/TWiki/TWikiDocGraphics/mail.gif', '/LICENSE']
                           },                           
                 "tikiwiki" : {"versionDirectoryRegex" : "tiki(?:wiki)?-(.*)",
                               "directoryExcludeRegex" : "backups|bin|db|error|templates|templates_c",
                               "fileExcludeRegex": ".*\.(?:php|php3|.sh)$",
                               "indicatorFiles" : ['/images/ico_clear.gif', '/lib/Galaxia/img/icons/mini_square.gif', '/img/icons/friend.gif', '/lib/Galaxia/img/icons/mini_blue_circle.gif']
                               },
                  "confluence" : {"versionDirectoryRegex" : "confluence-(.*)", 
                               "directoryExcludeRegex" : "WEB-INF",
                               "fileExcludeRegex": ".*\.(?:xml|jar|jsp|vm)$",
                               "indicatorFiles" : ['/images/raw/open-active.png', '/images/icons/arrow_block_16.gif', '/images/icons/list_pages_16.gif', '/images/icons/bullet_inprogress.gif']
                               },
                               
}

