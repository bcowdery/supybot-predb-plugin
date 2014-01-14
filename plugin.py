
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
        self._pre = pre.Releases('https://api.pre.im/v1.0/', accesskey, False)

    def _dupe(self, irc, query, group, section):
        self.log.info("dupe { search: %s, group: %s, section: %s }", query, group, section)
        limit = self.registryValue('limit')
        releases = self._pre.dupe(query, group, section, limit)

        irc.reply("Found {0} releases matching '{1}', sending a PM ...,".format(len(releases), query))
        for release in releases: irc.reply(release, private=True)

    def dupe(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Perform a search of the pre database for releases and returns all matches up to the
        configured limit. You can filter your search results by section (MP3, X264, etc) and
        by release group.
        """

        options = dict(optlist)
        group = options['group'] if 'group' in options else None
        section = options['section'] if 'section' in options else None
        self._dupe(irc, text, group, section)
    dupe = wrap(dupe, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])

    def _pre(self, irc, query, group, section):
        self.log.info("pre { search: %s, group: %s, section: %s }", query, group, section)
        releases = self._pre.dupe(query, group, section, 1)
        for release in releases: irc.reply(release, prefixNick=False)

    def pre(self, irc, msg, args, optlist, text):
        """[--section s] [--group g] <search>

        Perform a search of the pre database for a release. You can filter your
        search results by section (MP3, X264, etc) and by release group. Only returns
        a single release.
        """

        options = dict(optlist)
        group = options['group'] if 'group' in options else None
        section = options['section'] if 'section' in options else None
        self._pre(irc, text, group, section)
    pre = wrap(pre, [getopts({ 'group': 'something', 'section': 'something' }), 'text'])

Class = Pre
