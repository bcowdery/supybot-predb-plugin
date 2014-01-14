Supybot Pre.im Plugin
=====================

Plugin for the supybot IRC bot for checking scene releases against the pre database.

# Usage

`(dupe [--section s] [--group g] <search>)`
Search the pre database for all releases matching the search string. You can filter the search results by `--section` (e.g., MP3, X264, TV, TV-HD), and by release `--group`.

`(pre [--section s] [--group g] <search>)`
Search the pre database for a single releases matching the search string. You can filter the search results by `--section` (e.g., MP3, X264, TV, TV-HD), and by release `--group`. This operation is identical to `dupe`, but only returns a single result.

`(lastnukes [--section s] [--group g])`
Show recent releases that have been nuked. You can filter the search results by `--section` (e.g., MP3, X264, TV, TV-HD), and by release `--group`.

`(group <group>)` 
Fetch information about the first, last and number of releases for a specific group.


# Getting Started

## Installing the plugin

    $ cd ./plugins/
    $ git clone git@github.com:bcowdery/supybot-predupe-check.git Pre

## Configuring

If you create a new bot using `supybot-wizard` after installing the plugin, it should be available to configure
in the wizard. You'll be asked for the Pre.im accesskey and the limit of results to return from queries (default is 10).

You can also configure the plugin manually by editing your bot's config file
```conf
###
# Determines what plugins will be loaded.
#
# Default value:
###
supybot.plugins: Pre

###
# Determines whether this plugin is loaded by default.
###
supybot.plugins.Pre: True

###
# Determines whether this plugin is publicly visible.
#
# Default value: True
###
supybot.plugins.Pre.public: True

###
# Web API access key to be sent in HTTP headers when making database
# requests.
#
# Default value: deadbeef
###
supybot.plugins.Pre.accesskey: deadbeef

###
# Maximum number of results to return from the pre.im database. If the
# number of results found exceeds this value they will not be shown.
#
# Default value: 10
###
supybot.plugins.Pre.limit: 10
```

# Python dependencies

* [requests](http://docs.python-requests.org/)
* [Cheetah](http://www.cheetahtemplate.org/)

**Installation:**
```
$ pip install requests
$ pip install cheetah
```

# Documentation:

* [PRE.iM API Documentation](https://pre.im/doku/index.htm)

# License

Licensed under the MIT license.
