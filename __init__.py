"""
Keeps track of the last time a user was seen on a channel.
"""

import supybot
import supybot.world as world

__version__ = "0.0.1"
__author__ = "Batcow <bcowdery@pointyspoon.com>"

import config
import plugin
reload(plugin) # In case we're being reloaded.

if world.testing:
    import test

Class = plugin.Class
configure = config.configure
