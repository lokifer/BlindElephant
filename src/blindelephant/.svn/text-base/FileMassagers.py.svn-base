"""The following functions are simple transformers that can be used
 individually or in combination to modify (massage) the file found
 on the server to attempt to have it match what was originally hashed.
 
 They are used in instances where the file found doesn't match a 
 known fingerprint but might have been tampered with in a few predicatable
 ways. Undoing those changes might produce a valid fingerprint.

 This is not a robust, algorithmically intelligent way to do this, but it
 happens to work in enough cases to be worth trying as a fallback.
"""
#------------
# TODO:
# - add check functions to prevent expensive re/replace if modified constructs
#   don't even exist in file
#------------
import re


def changeLineEndings(data):
    return data.replace("\r\n", "\n")

def replaceCvsKeywords(data):
    keywords = ["Author", "Date", "Header", "Id", "Log", "Locker", "Name", 
                "RCSfile", "Revision", "Source", "State"]
    for w in keywords:
        data = re.sub("\$%s: [^$]*\$" % w, "$%s$" % w, data)
    return data
    
MASSAGERS = [changeLineEndings, replaceCvsKeywords]