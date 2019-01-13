#! /usr/bin/env python3

"""exploring categories."""

# imports ###################################################################

import sys
import getopt
import textwrap

from collections import defaultdict


# command line options ######################################################

name, args = sys.argv[0], sys.argv[1:]

DEFAULTS = {
	"category": None,
}

def exit_usage(message=None, code=0):
	usage = textwrap.dedent("""\
	Usage: %(name)s [-hc:]
		-h --help                  print this help message then exit
		-c --category <category>   list the products belonging to this category
	""" % dict(name=name, **DEFAULTS))
	if message:
		sys.stderr.write("%s\n" % message)
	sys.stderr.write(usage)
	sys.exit(code)

try:
	options, args = getopt.getopt(args, "hc:",
	                                    ["help", "category="])
except getopt.GetoptError as message:
	exit_usage(message, 1)

category = DEFAULTS["category"]

for opt, value in options:
	if opt in ["-h", "--help"]:
		exit_usage()
	elif opt in ["-c", "--category"]:
		category = value


# data ######################################################################

counts = defaultdict(int)
codes = []
categories = open("tsv/products_categories_full.tsv")

for header in categories:
	assert header.strip() == "code	category"
	break

for line in categories:
	code, cat = line.strip().split('\t')
	counts[cat] += 1
	if cat == category:
		codes.append(code)

if category == None: # categories counts
	for cat in sorted(counts, key=lambda k: counts[k]):
		count = counts[cat]
		if count < 2000: continue
		print('\t'.join(str(_) for _ in [cat, count]))
else:                # category content
	products = open("tsv/products.tsv")
	for header in products:
		sys.stdout.write(header)
		break
	for line in products:
		code, *_ = line.split('\t')
		if code in codes:
			sys.stdout.write(line)
