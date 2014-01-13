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
parser = argparse.ArgumentParser(description="Query Pre.im for the latest pres, nukes and unnukes")
parser.add_argument('-g', '--group', metavar='g', help='Filter results by group name (only applicable for nukes)')
parser.add_argument('-s', '--section', metavar='s', help='Search within a section, example: "mp3"')
parser.add_argument('-l', '--limit', metavar='n', type=int, default=10, help='Show N number of releases')
parser.add_argument('-p', '--pre', dest='pre', action='store_true', help="Show recent pres")
parser.add_argument('-n', '--nuke', dest='nuke', action='store_true', default=True, help='Show recent nukes')
parser.add_argument('-un', '--un-nuke', dest='nuke', action='store_false', help='Show recent un-nukes')

args = parser.parse_args()


# query
r = pre.Releases(url, accesskey, verify)
releases = None

if args.pre:
    releases = r.lastpres(args.section, args.limit)
elif args.nuke:
    releases = r.lastnukes(args.group, args.section, args.limit)
else:
    releases = r.lastunnukes(args.group, args.section, args.limit)

print releases
