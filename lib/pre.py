import urlparse, requests, json

class Releases:
    def __init__(self, url='https://api.pre.im/v1.0/', accesskey=None, verify=True):
        self.url       = url
        self.accesskey = accesskey
        self.verify    = verify

    def __headers(self):
        return {
            'Accesskey':    self.accesskey,
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def __request(self, method, options=None):
        url = urlparse.urljoin(self.url, method)
        r = requests.post(url, data=json.dumps(options), headers=self.__headers(), verify=self.verify)
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
        return self.__request('dupe', options)

    def edupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of latest releases (included deleted releases) that match the given query, with
        nuke and unnuke information.
        """
        options = { 'search': query }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        return self.__request('edupe', options)

    def rdupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of oldest releases that match the given query, with nuke and unnuke information.
        """
        options = { 'search': query }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        return self.__request('rdupe', options)

    def group(self, group):
        """
        Returns information about the first, last, and number of releases in the given group.
        """
        return self.__request('group', { 'group': group })

    def lastnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently nuked.
        """
        options = { }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        return self.__request('lastnukes', options)

    def lastpres(self, section=None, limit=None):
        """
        Returns a set of releases that have been recently pred.
        """
        options = { }
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        return self.__request('lastpres', options)

    def lastunnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently unnuked.
        """
        options = { }
        if group:   options['group'] = group
        if section: options['section'] = section
        if limit:   options['limit'] = limit
        return self.__request('lastunnukes', options)

    def nfo(self, search):
        """
        Searches for a release and returns a URL to the PreDB NFO Viewer. Depending on your API key it
        may be possible to download the NFO file from the viewer.
        """
        return self.__request('nfo', { 'search': search })

    def sections(self):
        """
        Returns a list of all sections in the pre database.
        """
        return self.__request('sections')

    def stats(self):
        """
        Returns some statistics about the pre database.
        """
        return self.__request('stats')
