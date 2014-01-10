#!/usr/bin/python
import ConfigParser
import urlparse, requests, json


# config
config = ConfigParser.ConfigParser()
config.readfp(open('pre.cfg'))

url    = config.get('PreDb', 'Url')
apikey = config.get('PreDb', 'ApiKey')
verify = config.getboolean('PreDb', 'VerifyCertificate')


# http request
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


# toss out extra junk in the response, just parse json blob
result = json.loads(r.text.split('\n')[-1])
print result
