import supybot.ircutils as irc

def files(r):
    """
    Prints the number of files and total size of the release as a 
    formatted string for IRC messages.
    """
    if r.files or r.size:
        return "%s%d/%d%s" % (irc.bold('F'), r.files, r.size, irc.bold('MB'))    
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
