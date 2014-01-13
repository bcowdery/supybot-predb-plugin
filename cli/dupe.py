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
parser = argparse.ArgumentParser(description="Query Pre.im for releases")
parser.add_argument('-q', '--query', metavar='q', required=True, help='The query to search for (required)')
parser.add_argument('-g', '--group', metavar='g', help='Filter results by group name')
parser.add_argument('-s', '--section', metavar='s', help='Search within a section, example: "mp3"')
parser.add_argument('-l', '--limit', metavar='n', type=int, default=10, help='Show N number of releases')
parser.add_argument('-e', '--deleted', action='store_true', help='edupe - Include deleted releases')
parser.add_argument('-r', '--oldest', action='store_true', help='rdupe - Search for the oldest releases')

args = parser.parse_args()


# query
r = pre.Releases(url, accesskey, verify)
releases = None

if args.deleted:
    releases = r.edupe(args.query, args.group, args.section, args.limit)
elif args.oldest:
    releases = r.rdupe(args.query, args.group, args.section, args.limit)
else:
    releases = r.dupe(args.query, args.group, args.section, args.limit)

for r in releases:
    print r
