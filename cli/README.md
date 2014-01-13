Pre.im Command Line Scripts
===========================

Command line scripts for quering the pre database.


# Usage

## Dupes

Query Pre.im for releases that match your search term with nuke and unnuke information.

```
$ python dupe.py --query "the matrix"
```

* `-q q, --query q`   The query to search for (required)
* `-g g, --group g`   Filter results by group name
* `-s s, --section s` Search within a section, example: "mp3"
* `-l n, --limit n`   Show N number of releases
* `-e, --deleted`     *edupe* - Include deleted releases
* `-r, --oldest`      *rdupe* - Search for the oldest releases

## Recent nukes, un-nukes and pres

Query Pre.im for the latest pres, nukes and unnukes

```
$ python last.py [--pre] [--nuke] [--un-nuke]
```

* `-g g, --group g`   Filter results by group name (only applicable for nukes)
* `-s s, --section s` Search within a section, example: "mp3"
* `-l n, --limit n`   Show N number of releases
* `-p, --pre`         Show recent pres
* `-n, --nuke`        Show recent nukes
* `-un, --un-nuke`    Show recent un-nukes
* `--print-reason`    Print the latest reason this release was nuked/unnuked

## Group

Query Pre.im for the first, last and number of releases for a group.

```
$ python group.py --group "NoTV"
```

* `-g g, --group g` Show stats for group name

## Pre database stats

Query generic Pre.im database information.

```
$ python stats.py
```

* `-s, --sections` List all sections in the database

## NFO

Get the PreDB NFO Viewer URL for a release (if available).

```
$ python nfo.py --release "Futurama.S07E26.1080p.BluRay.x264-ROVERS"
```

* `-r, --release` The release name to get the NFO for


# Configuration

A sample configuration file `pre.cfg.sample` is provided. Rename the file to 'pre.cfg', fill in your Pre.im Accesskey
and you're good to go.

```config
[PreDb]
ApiKey: deadbeef123
Url: https://api.pre.im/v1.0/
VerifyCertificate: True
```

* `ApiKey` - PRE.iM Accesskey
* `Url` - Url endpoint for the PRE.iM API
* `VerifyCertificate` - Set to 'False' to ignore SSL certificate errors

_Note: Do not disable SSL certificate verification unless you know what you are doing! Typically updating your machines
certificate store is enough to solve most SSL verification errors_


# License

Licensed under the MIT license.
