#!/usr/bin/python
# coding=utf-8

import argparse
import os.path
import sys

sys.path = [sys.path[0]] + [os.path.join(os.path.dirname(__file__), "../lib")] + sys.path[1:]
import DataProcessor
sys.path = [sys.path[0]] + sys.path[2:]


def main():
    parser = argparse.ArgumentParser(description="command line interface for DataProcessor pipeline")
    parser.add_argument('json_filename')
    args = parser.parse_args()

    if not os.path.exists(args.json_filename):
        print("such file does not exists")
        return 1
    with open(args.json_filename, 'r') as f:
        DataProcessor.execute_from_json_str(f.read())

if __name__ == "__main__":
    main()
