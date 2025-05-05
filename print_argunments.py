#!.usr/bin/python3
import sys

args = sys.argv[1:] # skip script name

print("Number of arguments:", len(args))
for arg in args:
    print(arg)
