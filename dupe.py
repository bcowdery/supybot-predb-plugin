#!/usr/bin/python
import argparse, ConfigParser
import urlparse, requests, json


# command line args
parser = argparse.ArgumentParser(description="Query PRE.iM for duplicate releases")
parser.add_argument('-q', '--query', metavar='q', help='The query to search for')
parser.add_argument('-l', '--limit', metavar='n', type=int, required=False, default=10, help='Show x number of releases')

args = parser.parse_args()


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
    'search': args.query,
    'limit': args.limit
}

r = requests.post(urlparse.urljoin(url, 'dupe'), data=json.dumps(payload), headers=headers, verify=verify)
r.raise_for_status()


# toss out extra junk in the response, just parse json blob
result = json.loads(r.text.split('\n')[-1])
print result
