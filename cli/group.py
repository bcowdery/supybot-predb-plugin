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
parser = argparse.ArgumentParser(description="Query PRE.iM for group information")
parser.add_argument('-g', '--group', metavar='g', help='Show stats for group name')
args = parser.parse_args()

# query
r = pre.Releases(url, accesskey, verify)
print r.group(args.group)
