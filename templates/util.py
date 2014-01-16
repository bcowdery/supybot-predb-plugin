import supybot.ircutils as irc
import datetime

def files(r):
    """
    Prints the number of files and total size of the release as a 
    formatted string for IRC messages.
    """
    if r.files or r.size:
        return "%sF/%sMB" % (irc.bold(r.files), irc.bold(r.size))    
    return irc.mircColor('?', fg=7)
    
def status(r):
    """
    Prints the textual status of a release as a formatted string for IRC messages.
    """
    latest = r.last_nuke()
    if latest:
        if latest.isnuke:
            return irc.bold(irc.mircColor('NUKED', fg=7))
        else:
            return irc.bold(irc.mircColor('UNNUKED', fg=3))
    return irc.bold('PRE')

def age(r):
    """
    Prints the age of this release in the format "0d 0h 0mi 0s".
    """
    total_seconds = (datetime.datetime.now() - r.time).total_seconds()        
    if total_seconds > 0:
        days, seconds = divmod(total_seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        if days > 0:
            return "%dd %dh %dmi %ds" % (days, hours, minutes, seconds)
        if hours > 0:
            return "%dh %dmi %ds" % (hours, minutes, seconds)
        if minutes > 0:
            return "%dmi %ds" % (minutes, seconds)
        if seconds > 0:
            return "%ds" % (seconds)
    return irc.mircColor('0s', fg=7)
