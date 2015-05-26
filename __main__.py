#!/usr/bin/python2

import os
import sys
import argparse
from recognizer import *
from solver import *
from gui import *

parser = argparse.ArgumentParser(prog="detector_test")
parser.add_argument("-d", "--database", nargs=1, help="face database")
parser.add_argument("-t", "--threshold", nargs=1, default=[0.50], \
	type=float, help="threshold value(default: 0.5)")
parser.add_argument("--gui", action="store_true")
parser.add_argument("testimgs", nargs="*", help="test picture directory")

def startcli(args):
	dburl = args.database[0]
	testimgs = args.testimgs
	
	th = args.threshold[0]
	if th > 1: th = 1.0

	db = SRCFaceDatabase(dburl)
	recognizer = SRCFaceRecognizer(DALMSolver())

	print("==== start recognize ====")
	print("%-30s%-10s%s" % ('[path]', '[class]', '[sci]'))

	count = 0
	total = 0

	for i in imgs:
		total += 1
		d,s = recognizer.recognize(db, imread(i))
		if s < th: continue
		if d['class'] in i:
			print("%-30s%-10s%.2f" % (i, d["class"], s))
		count += 1

	print("result: %d/%d (%.2f%%), threshold: %.2f" % (count, total, (float(count)/total)*100, th))

def main():
	args = parser.parse_args(sys.argv[1:])
	return startgui() if args.gui else startcli(args)

if __name__ == "__main__":
	sys.exit(main())