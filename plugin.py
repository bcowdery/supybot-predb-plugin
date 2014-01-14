
from lib import pre

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

class Pre(callbacks.Plugin):
    def __init__(self, irc=None):
        self.__parent = super(Pre, self)
        self.__parent.__init__(irc)

        accesskey = self.registryValue('accesskey')
        self._predb = pre.Releases('https://api.pre.im/v1.0/', accesskey, False)

    def _dupe(self, search, optlist, limit):
        options = dict(optlist)
        group = options['group'] if 'group' in options else None
        section = options['section'] if 'section' in options else None

        self.log.info("dupe { search: %s, group: %s, section: %s, limit: %s}", search, group, section, limit)
        return self._predb.dupe(search, group, section, limit)

    def dupe(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Perform a search of the pre database for releases and returns all matches up to the
        configured limit. You can filter your search results by section (MP3, X264, etc) and
        by release group.
        """

        limit = self.registryValue('limit')
        releases = self._dupe(text, optlist, limit)
        if releases:
            irc.reply("Found {0} releases matching '{1}', sending a PM ...".format(len(releases), text))
            for release in releases: irc.reply(release, private=True)
        else:
            irc.reply("Couldn't find any releases matching '{0}'".format(text))

    dupe = wrap(dupe, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])

    def pre(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Perform a search of the pre database for a single release. You can filter your
        search results by section (MP3, X264, etc) and by release group. Only returns
        a single release.
        """

        releases = self._dupe(text, optlist, 1)
        if releases:
            for release in releases: irc.reply(release, prefixNick=False)
        else:
            irc.reply("Couldn't find any releases matching '{0}'".format(text))

    pre = wrap(pre, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])

    def group(self, irc, msg, args, text):
        """<group>

        Fetch information about the first, last and number of releases for a specific group
        """

        self.log.info("group { group: %s }", text)

        group = self._predb.group(text)
        if group:
            irc.reply("{0} has {1} releases".format(text, group.releases), prefixNick=False)
            irc.reply("First:  {0}".format(group.first), prefixNick=False)
            irc.reply("Latest: {0}".format(group.last), prefixNick=False)
        else:
            irc.reply("Couldn't find group '{0}'".format(text))

    group = wrap(group, ['text'])

    def lastnukes(self, irc, msg, args, optlist):
        """[--section s] [--group g]

        Show recent nukes up to the configured limit. You can filter search results by
        section and by release group.
        """

        options = dict(optlist)
        group = options['group'] if 'group' in options else None
        section = options['section'] if 'section' in options else None

        limit = self.registryValue('limit')

        self.log.info("lastnukes { group: %s, section: %s, limit: %s}", group, section, limit)

        releases = self._predb.lastnukes(group, section, limit)
        if releases:
            irc.reply("Sending last {0} nukes in a PM ...".format(len(releases)))
            for release in releases:
                irc.reply(release, private=True)
                irc.reply(release.last_nuke(), private=True)
        else:
            irc.reply("No nukes.")

    lastnukes = wrap(lastnukes, [getopts({ 'group': 'something', 'section': 'something' })])

Class = Pre
