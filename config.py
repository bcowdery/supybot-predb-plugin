import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Pre', True)

Pre = conf.registerPlugin('Pre')

conf.registerGlobalValue(Pre, 'accesskey',
    registry.String('deadbeef',
                    """Web API access key to be sent in HTTP headers when
                       making database requests."""))

conf.registerGlobalValue(Pre, 'limit',
    registry.String('10',
                    """Maximum number of results to return from the pre.im
                       database. If the number of results found exceeds this
                       value they will not be shown."""))
