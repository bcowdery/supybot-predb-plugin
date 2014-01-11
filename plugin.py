import pre

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


class Dupe(callbacks.Plugin):
    noIgnore = True
    def __init__(self, irc):
        self.__parent = super(Seen, self)
        self.__parent.__init__(irc)

    def die(self):
        self.__parent.die()

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)

    def _seen(self, irc, channel, name, any=False):
        results = pre.dupe(name, 10)
        if (results):
            irc.reply(format('I haven\'t seen anyone matching %s.', name))
        else:
            irc.reply(format('Could not find any results for %s.', name))

    def dupe(self, irc, msg, args, channel, name):
        """<name>

        Searches for scene dupes by <name>.
        """
        self._dupe(irc, channel, name)
    dupe = wrap(dupe, ['channel', 'something'])

Class = Dupe
