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

from lib import pre

class Pre(callbacks.Plugin):

    def __init__(self):
        url = self.registryValue('url')
        accesskey = self.registryValue('accesskey')
        self._predb = pre.Releases(url=url, accesskey=accesskey)

    def _dupe(self, irc, query, limit):
        results = self._predb.dupe(query, limit)
        if (results):
            irc.reply(format('Got %s.', results.length))
            irc.reply(format('Results %s', results), private=True)
        else:
            irc.reply(format('Could not find any results for %s.', name))

    def dupe(self, irc, msg, args, text):
        """dupe <search>

        Perform a search for dupe releases using Pre.im's Web API
        """
        limit = self.registryValue('limit', msg.args[0])
        self._dupe(irc, text, limit)
    dupe = wrap(dupe, ['text'])

Class = Pre
