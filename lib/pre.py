import ConfigParser
import urlparse, requests, json

CFG_SECTION = 'pre'

class Releases:
    def __init__(self, url=None, accesskey=None, verify=None):
        config = ConfigParser.ConfigParser()
        config.read('pre.cfg')

        self.url = config.get(CFG_SECTION, 'Url') if not url else url
        self.accesskey = config.get(CFG_SECTION, 'AccessKey') if not accesskey else accesskey
        self.verify = config.getboolean(CFG_SECTION, 'VerifyCertificate') if verify == None else verify

    def __headers(self):
        return {
            'Accesskey':    self.accesskey,
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def __request(self, method, options):
        print self.url
        print self.accesskey
        print self.verify

        url = urlparse.urljoin(self.url, method)
        r = requests.post(url, data=json.dumps(options), headers=self.__headers(), verify=self.verify)
        r.raise_for_status()
        return r

    def dupe(self, query, limit):
        r = self.__request('dupe', { 'search': query, 'limit': limit })
        if r.text: return json.loads(r.text.split('\n')[-1])



