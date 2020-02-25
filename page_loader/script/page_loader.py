#!/usr/bin/env python3
import argparse
from page_loader.engine import loader


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for output', type=str)
    args = parser.parse_args()
    loader(args.url, args.output)


if __name__ == '__main__':
    main()
