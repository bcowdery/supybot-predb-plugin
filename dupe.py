import ConfigParser
import urlparse
import requests
import json

config = ConfigParser.ConfigParser()
config.readfp(open('pre.cfg'))

url    = config.get('PreDb', 'Url')
apikey = config.get('PreDb', 'ApiKey')
verify = config.getboolean('PreDb', 'VerifyCertificate')

headers = {
    'Accesskey': apikey,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

payload = {
    'search': 'eyes wide shut',
    'limit': 10
}

r = requests.post(urlparse.urljoin(url, 'dupe'), data=json.dumps(payload), headers=headers, verify=verify)
r.raise_for_status()

print r.content
