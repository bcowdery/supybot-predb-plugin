#!/usr/bin/python
import argparse
import pre

# command line args
parser = argparse.ArgumentParser(description="Query PRE.iM for duplicate releases")
parser.add_argument('-q', '--query', metavar='q', required=True, help='The query to search for (required)')
parser.add_argument('-l', '--limit', metavar='n', type=int, default=10, help='Show x number of releases')

args = parser.parse_args()

# query
print pre.dupe(args.query, args.limit)
