#!/usr/bin/env python3

from sys import version_info

if (version_info[0],version_info[1]) < (3,6):
	print("\nScript requires python version >= 3.6 .\nTry running following command: 'python3 run.py'\n")
	exit(0)

import bundler
