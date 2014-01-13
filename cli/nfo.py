#!/usr/bin/python
import sys, os
import ConfigParser, argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
import pre


# config files
config = ConfigParser.SafeConfigParser()
config.read('pre.cfg')

url       = config.get('pre', 'Url')
accesskey = config.get('pre', 'Accesskey')
verify    = config.get('pre', 'VerifyCertificate')


# command line args
parser = argparse.ArgumentParser(description="URL to the PreDB NFO Viewer")
parser.add_argument('-r', '--release', metavar='q', required=True, help='The release name to get the NFO for')
args = parser.parse_args()

# query
r = pre.Releases(url, accesskey, verify)
print r.nfo(args.release)
