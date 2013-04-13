#!/usr/bin/python
# coding=utf-8

import argparse
import os.path
import pipes

def main():
    parser = argparse.ArgumentParser(description="command line interface for DataProcessor pipeline")
    parser.add_argument('json_filename')
    args = parser.parse_args()

    if not os.path.exists(args.json_filename):
        print("such file does not exists")
        return 1
    with open(args.json_filename,'r') as f:
        pipes.execute_from_json_str(f.read())

if __name__ == "__main__":
    main()
