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
verify    = config.getboolean('pre', 'VerifyCertificate')


# command line args
parser = argparse.ArgumentParser(description="Show Pre.im database information")
parser.add_argument('-s', '--sections', action='store_true', help='List all sections in the database')
args = parser.parse_args()

# query
r = pre.Releases(url, accesskey, verify)



# print the results
if args.sections:
    sections = r.sections()
    for section in sections: print section
else:
    stats = r.stats()
    print stats
