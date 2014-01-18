
import sys, os
from lib import pre
from Cheetah.Template import Template

import supybot.log as log
import supybot.conf as conf
import supybot.utils as utils
import supybot.world as world
import supybot.ircdb as ircdb
from supybot.commands import *
import supybot.irclib as irclib
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
sys.path.append(TEMPLATE_DIR)

_release_template = Template(file=os.path.join(TEMPLATE_DIR, 'release.tmpl'))
def format_releases(releases):
    _release_template.releases = releases
    return str(_release_template).strip()

_group_template = Template(file=os.path.join(TEMPLATE_DIR, 'group.tmpl'))
def format_group(group):
    _group_template.g = group
    return str(_group_template).strip()

_stats_template = Template(file=os.path.join(TEMPLATE_DIR, 'stats.tmpl'))
def format_stats(stats):
    _stats_template.s = stats
    return str(_stats_template).strip()

def write(irc, message, prefixNick=None, private=None):    
    if message:
        for line in message.split('\n'):
            if line: irc.reply(line, prefixNick=prefixNick, private=private)


class Options():
    def __init__(self, optlist):
        options = dict(optlist)                
        self.group   = options['group'] if 'group' in options else None
        self.section = options['section'] if 'section' in options else None        


class Pre(callbacks.Plugin):
    def __init__(self, irc=None):
        self.__parent = super(Pre, self)
        self.__parent.__init__(irc)

        self.limit = self.registryValue('limit')
        self.accesskey = self.registryValue('accesskey')
        self._predb = pre.Releases('https://api.pre.im/v1.0/', self.accesskey, False)
    

    def dupe(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Search the pre database for all releases matching the search string. You can filter
        the search results by --section (e.g., MP3, X264, TV, TV-HD), and by release --group.
        """

        options = Options(optlist)
        self.log.info("dupe { search: %s, group: %s, section: %s }", text, options.group, options.section)

        releases = self._predb.dupe(text, options.group, options.section, self.limit)
        if releases:
            irc.reply("Found {0} releases matching '{1}', sending a PM ...".format(len(releases), text))            
            write(irc, format_releases(releases), private=True)                
        else:
            irc.reply("Couldn't find any releases matching '{0}'".format(text))

    dupe = wrap(dupe, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])


    def pre(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Search the pre database for a single releases matching the search string. You can filter
        the search results by --section (e.g., MP3, X264, TV, TV-HD), and by release --group. This
        operation is identical to (dupe <search>), but only returns a single result.
        """

        options = Options(optlist)
        self.log.info("pre { search: %s, group: %s, section: %s }", text, options.group, options.section)

        releases = self._predb.dupe(text, options.group, options.section, 1)
        if releases:
            write(irc, format_releases(releases), prefixNick=False)
        else:
            irc.reply("Couldn't find any releases matching '{0}'".format(text))

    pre = wrap(pre, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])


    def group(self, irc, msg, args, text):
        """<group>

        Fetch information about the first, last and number of releases for a specific group.
        """

        self.log.info("group { group: %s }", text)

        group = self._predb.group(text)
        if group:
            write(irc, format_group(group), prefixNick=False)
        else:
            irc.reply("Couldn't find group '{0}'".format(text))

    group = wrap(group, ['text'])


    def nfo(self, irc, msg, args, text):
        """<release>

        Searches for a release and returns a URL to the PreDB NFO Viewer. Depending on your API key it
        may be possible to download the NFO file from the viewer.
        """

        self.log.info("nfo { search: %s }", text)

        url = self._predb.nfo(text)
        if url:
            irc.reply("NFO: {0}".format(url))
        else:
            irc.reply("Sorry, couldn't find an NFO for '{0}'".format(text))

    nfo = wrap(nfo, ['text'])


    def lastnukes(self, irc, msg, args, optlist):
        """[--section s] [--group g]

        Show recent releases that have been nuked. You can filter the search results
        by --section (e.g., MP3, X264, TV, TV-HD), and by release --group.
        """
        
        options = Options(optlist)
        self.log.info("lastnukes { group: %s, section: %s }", options.group, options.section)
        
        releases = self._predb.lastnukes(options.group, options.section, self.limit)
        if releases:
            irc.reply("Sending last {0} nukes in a PM ...".format(len(releases)))            
            write(irc, format_releases(releases), private=True)
        else:
            irc.reply("No recent nukes found.")

    lastnukes = wrap(lastnukes, [getopts({ 'group': 'something', 'section': 'something' })])


    def lastunnukes(self, irc, msg, args, optlist):
        """[--section s] [--group g]

        Show recent releases that have been un-nuked. You can filter the search results
        by --section (e.g., MP3, X264, TV, TV-HD), and by release --group.
        """
        
        options = Options(optlist)
        self.log.info("lastunnukes { group: %s, section: %s }", options.group, options.section)
        
        releases = self._predb.lastunnukes(options.group, options.section, self.limit)
        if releases:
            irc.reply("Sending last {0} un-nukes in a PM ...".format(len(releases)))
            write(irc, format_releases(releases), private=True)
        else:
            irc.reply("No recent un-nukes found.")

    lastunnukes = wrap(lastunnukes, [getopts({ 'group': 'something', 'section': 'something' })])


    def lastpres(self, irc, msg, args, optlist):
        """[--section s]

        Show recent releases that have been pred. You can filter the search results
        by --section (e.g., MP3, X264, TV, TV-HD).
        """
        
        options = Options(optlist)
        self.log.info("lastpres { section: %s }", options.section)
        
        releases = self._predb.lastpres(options.section, self.limit)
        if releases:
            irc.reply("Sending last {0} pres in a PM ...".format(len(releases)))            
            write(irc, format_releases(releases), private=True)
        else:
            irc.reply("No recent pres found.")

    lastpres = wrap(lastpres, [getopts({ 'section': 'something' })])


    def predb(self, irc, msg, args):
        """Show some statistics about the pre database"""

        self.log.info("stats { }")

        stats = self._predb.stats()
        if stats:
            write(irc, format_stats(stats), prefixNick=False)
        else:
            irc.reply("No stats available.")

    predb = wrap(predb)


Class = Pre
