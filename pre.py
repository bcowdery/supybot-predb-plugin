import ConfigParser
import urlparse, requests, json

CFG_SECTION = 'PreDb'

def __conf():
    config = ConfigParser.ConfigParser()
    config.readfp(open('pre.cfg'))
    return {
        'url':    config.get(CFG_SECTION, 'Url'),
        'apikey': config.get(CFG_SECTION, 'ApiKey'),
        'verify': config.getboolean(CFG_SECTION, 'VerifyCertificate')
    }

def __headers(apikey):
    return {
        'Accesskey':    apikey,
        'Accept':       'application/json',
        'Content-Type': 'application/json'
    }

def __request(method, options):
    config  = __conf()
    headers = __headers(config['apikey'])
    url     = urlparse.urljoin(config['url'], method)

    r = requests.post(url, data=json.dumps(options), headers=headers, verify=config['verify'])
    r.raise_for_status()
    return r



def dupe(query, limit):
    r = __request('dupe', { 'search': query, 'limit': limit })
    return json.loads(r.text.split('\n')[-1])



