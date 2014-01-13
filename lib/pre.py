import ConfigParser
import urlparse, requests, json

CFG_SECTION = 'pre'

class Releases:
    def __init__(self, url=None, accesskey=None, verify=None):
        config = ConfigParser.ConfigParser()
        config.read('pre.cfg')

        self.url       = config.get(CFG_SECTION, 'Url') if not url else url
        self.accesskey = config.get(CFG_SECTION, 'AccessKey') if not accesskey else accesskey
        self.verify    = config.getboolean(CFG_SECTION, 'VerifyCertificate') if verify == None else verify

    def __headers(self):
        return {
            'Accesskey':    self.accesskey,
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def __request(self, method, options):
        url = urlparse.urljoin(self.url, method)
        r = requests.post(url, data=json.dumps(options), headers=self.__headers(), verify=self.verify)
        r.raise_for_status()
        return r


    # API methods

    def dupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of latest releases that match the given query, with nuke and unnuke information. The
        dupe method ignores deleted releases.
        """
        options = { 'search': query }
        if not group:   options['group'] = group
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('dupe', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def edupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of latest releases (included deleted releases) that match the given query, with
        nuke and unnuke information.
        """
        options = { 'search': query }
        if not group:   options['group'] = group
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('edupe', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def rdupe(self, query, group=None, section=None, limit=None):
        """
        Returns a set of oldest releases that match the given query, with nuke and unnuke information.
        """
        options = { 'search': query }
        if not group:   options['group'] = group
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('rdupe', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def group(self, group):
        """
        Returns information about the first, last, and number of releases in the given group.
        """
        r = self.__request('group', { 'group': group })
        if r.text: return json.loads(r.text.split('\n')[-1])

    def lastnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently nuked.
        """
        options = { }
        if not group:   options['group'] = group
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('lastnukes', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def lastpre(self, section=None, limit=None):
        """
        Returns a set of releases that have been recently pred.
        """
        options = { }
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('lastpre', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def lastunnukes(self, group=None, section=None, limit=None):
        """
        Returns a set of releases that have been recently unnuked.
        """
        options = { }
        if not group:   options['group'] = group
        if not section: options['section'] = section
        if not limit:   options['limit'] = limit

        r = self.__request('lastunnuke', options)
        if r.text: return json.loads(r.text.split('\n')[-1])

    def nfo(self, search):
        """
        Searches for a release and returns a URL to the PreDB NFO Viewer. Depending on your API key it
        may be possible to download the NFO file from the viewer.
        """
        r = self.__request('nfo', { 'search': search })
        if r.text: return json.loads(r.text.split('\n')[-1])

    def sections(self):
        """
        Returns a list of all sections in the pre database.
        """
        r = self.__request('sections')
        if r.text: return json.loads(r.text.split('\n')[-1])

    def stats(self):
        """
        Returns some statistics about the pre database.
        """
        r = self.__request('stats')
        if r.text: return json.loads(r.text.split('\n')[-1])
