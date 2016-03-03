#!/usr/bin/python2

import os
import sys
import argparse
from classifier import *
from solver import *
from gui import *

parser = argparse.ArgumentParser(prog="detector_test")
parser.add_argument("-c", "--count", nargs=1, default=[1000], type=int, help="iteration count")
parser.add_argument("-d", "--database", nargs=1, help="face database")
parser.add_argument("-s", "--dbimgsize", nargs=1, default=[16], type=int, help="db image size [15, 100]")
parser.add_argument("-t", "--threshold", nargs=1, default=[0.50], \
	type=float, help="threshold value(default: 0.5)")
parser.add_argument("--gui", action="store_true", help="gui mode")
parser.add_argument("testimgs", nargs="*", help="test images")

class bcolors:
	HEADER = '\033[95m'
	BOLD = '\033[1m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

def startcli(args):
	maxiter = args.count[0]
	dburl = args.database[0]
	testimgs = args.testimgs

	dbimgsize = args.dbimgsize[0]
	if dbimgsize < 15: dbimgsize = 15
	if dbimgsize > 100: dbimgsize = 100

	th = args.threshold[0]
	if th > 1: th = 1.0

	db = SRCFaceDatabase(dburl)
	classifier = SRCFaceClassifier(DALMSolver())

	print("==== start classify ====")
	print("%-40s%-10s%s" % ('[path]', '[class]', '[sci]'))

	scount = 0
	ncount = 0
	total = 0

	for i in testimgs:
		total += 1
		d,s = classifier.classify(db, imread(i), (dbimgsize, dbimgsize), maxiter=maxiter)
		header, endc = "", ""
		if d['class'] in i:
			ncount += 1
			s = float("%.2f"%s)
			if s >= th: scount += 1
			else: header, endc = bcolors.WARNING, bcolors.ENDC
		else:
			header, endc = bcolors.FAIL, bcolors.ENDC
		print(header + "%-40s%-10s%.2f" % (i, d["class"], s) + endc)

	print(bcolors.BOLD + "result " + bcolors.ENDC + "total: %d, threshold: %.2f, maxiter: %d, dbimgsize: (%dx%d)" % (total, th, maxiter, dbimgsize, dbimgsize))
	print("	  strict: %d/%d (%.2f%%)" % (scount, total, (float(scount)/total)*100))
	print("	  normal: %d/%d (%.2f%%)" % (ncount, total, (float(ncount)/total)*100))

def main():
	args = parser.parse_args(sys.argv[1:])
	return startgui() if args.gui else startcli(args)

if __name__ == "__main__":
	sys.exit(main())
