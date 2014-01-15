import urlparse, requests, json
import datetime


def to_releases(list):
    if list:
        return [Release(r) for r in list ]
    return []

def to_sections(list):
    if list:
        return [ Section(s) for s in list ]
    return []          


class Releases:
    def __init__(self, url='https://api.pre.im/v1.0/', accesskey=None, verify=True):
        self.url       = url
        self.accesskey = accesskey
        self.verify    = verify

    def _headers(self):
        return {
            'Accesskey':    self.accesskey,
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def _request(self, method, options=None):
        url = urlparse.urljoin(self.url, method)
        r = requests.post(url, data=json.dumps(options), headers=self._headers(), verify=self.verify)
        r.raise_for_status()
        if r.text: return json.loads(r.text.split('\n')[-1])


    # Pre.IM Web API methods

    def dupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of latest releases that match the given query, with nuke and unnuke information. The
        dupe method ignores deleted releases.
        """
        options = { 'search': query }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('dupe', options)
        return to_releases(r);

    def edupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of latest releases (included deleted releases) that match the given query, with
        nuke and unnuke information.
        """
        options = { 'search': query }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('edupe', options)
        return to_releases(r)

    def rdupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of oldest releases that match the given query, with nuke and unnuke information.
        """
        options = { 'search': query }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('rdupe', options)
        return to_releases(r)

    def group(self, group):
        """
        Returns information about the first, last, and number of releases in the given group.
        """
        r = self._request('group', { 'group': group })
        return Group(group, r)

    def lastnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently nuked.
        """
        options = { }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('lastnukes', options)
        return to_releases(r);

    def lastpres(self, section=None, limit=None):
        """
        Returns a set of releases that have been recently pred.
        """
        options = { }
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('lastpres', options)
        return to_releases(r);

    def lastunnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently unnuked.
        """
        options = { }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        r = self._request('lastunnukes', options)
        return to_releases(r);

    def nfo(self, search):
        """
        Searches for a release and returns a URL to the PreDB NFO Viewer. Depending on your API key it
        may be possible to download the NFO file from the viewer.
        """
        return self._request('nfo', { 'search': search })

    def sections(self):
        """
        Returns a list of all sections in the pre database.
        """
        r = self._request('sections')
        return to_sections(r)

    def stats(self):
        """
        Returns some statistics about the pre database.
        """
        r = self._request('stats')
        return Stats(r)


class Release:
    def __init__(self, dict):
        self.release   = dict['release']
        self.section   = dict['section']
        self.genre     = dict['genre']
        self.files     = dict['files']
        self.size      = dict['size']
        self.time      = datetime.datetime.utcfromtimestamp(dict['time'])
        self.nukes     = [ Nuke(self, nuke) for nuke in dict['nukes']] if dict['nukes'] else []
        
    def last_nuke(self):
        """
        Sorts the list of nukes by datetime and returns the last (newest) 
        nuke status if any.
        """
        if self.nukes:
            self.nukes.sort(key=lambda n: n.time)
            return self.nukes[-1]

    def status(self):
        """
        Returns the current status of this release, PRE/NUKED/UNNUED,
        based on the last nuke if any. 
        """
        latest = self.last_nuke()
        if latest:
            if latest.isnuke:
                return "NUKED"
            else:
                return "UNNUKED"
        return "PRE"

    def age(self):
        """
        Returns the age of this release in the format "0d 0h 0mi 0s".
        """
        total_seconds = (datetime.datetime.now() - self.time).total_seconds()
        days, seconds = divmod(total_seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return "%dd %dh %dmi %ds" % (days, hours, minutes, seconds)

    def __str__(self):
        return "[{0}/{1}] {2} [{3}] [F{4}/{5}MB] [{6}]".format(self.status(), self.section, self.release, self.age(), self.files, self.size, self.time)


class Nuke:
    def __init__(self, release, dict):
        self.__parent__ = release
        self.isnuke     = dict['isnuke']
        self.ismodnuke  = dict['ismodnuke']
        self.reason     = dict['reason']
        self.network    = dict['network']
        self.time       = datetime.datetime.utcfromtimestamp(dict['time'])

    def __str__(self):
        status = "Nuked" if self.isnuke else "Unnuked"
        return "* {0} on {1} [{2}] -- {3}".format(status, self.time, self.network, self.reason)


class Section:
    def __init__(self, dict):
        self.section = dict['section']
        self.count   = dict['count']

    def __str__(self):
        return "\t{0:<20} \t{1}".format(self.section, self.count)


class Stats:
    def __init__(self, dict):
        self.releases = dict['releases']
        self.nukes = dict['nukes']
        self.unnukes = dict['unnukes']
        self.deletes = dict['deletes']
        self.undeletes = dict['undeletes']
        self.first = Release(dict['first'])
        self.last = Release(dict['last'])

    def __str__(self):
        return """
        Releases:  {0}
        Nukes:     {1}
        Unnukes:   {2}
        Deletes:   {3}
        UnDeletes: {4}
        First:     {5}
        Latest:    {6}
        """.format(self.releases, self.nukes, self.unnukes, self.deletes, self.undeletes, self.first, self.last)


class Group:
    def __init__(self, group, dict):
        self.group = group
        self.releases = dict['releases']
        self.first = Release(dict['first'])
        self.last = Release(dict['last'])

    def __str__(self):
        return """
        Releases:  {0}
        First:     {1}
        Latest:    {2}
        """.format(self.releases, self.first, self.last)
