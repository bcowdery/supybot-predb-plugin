
import os
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

_release_template = Template(file=os.path.join(TEMPLATE_DIR, 'release.tmpl'))
def format_release(release):
    _release_template.r = release
    return str(_release_template).strip()

_group_template = Template(file=os.path.join(TEMPLATE_DIR, 'group.tmpl'))
def format_group(group):
    _group_template.g = group
    return str(_group_template).strip()

_nuke_template = Template(file=os.path.join(TEMPLATE_DIR, 'nuke.tmpl'))
def format_nuke(release):
    _nuke_template.r = release
    return str(_nuke_template).strip()

def write(irc, message, prefixNick=None, private=None):
    for line in message.split('\n'):
        irc.reply(line, prefixNick=prefixNick, private=private)


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
            for release in releases: 
                write(irc, format_release(release), private=True)                
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
            for release in releases: 
                write(irc, format_release(release), prefixNick=False)
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
            irc.reply("Couldn't find group '{0}'", text)

    group = wrap(group, ['text'])


    def nfo(self, irc, msg, args, text):
        """<release>

        Searches for a release and returns a URL to the PreDB NFO Viewer. Depending on your API key it
        may be possible to download the NFO file from the viewer.
        """

        self.log.info("nfo { search: %s }".format(text))

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
            for release in releases: 
                write(irc, format_nuke(release), private=True)
        else:
            irc.reply("No nukes.")

    lastnukes = wrap(lastnukes, [getopts({ 'group': 'something', 'section': 'something' })])

Class = Pre
