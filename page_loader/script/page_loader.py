#!/usr/bin/env python3
import argparse
import os

from page_loader.engine import loader


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', help='set path for output', type=str,
                        default=os.path.join(os.getcwd(), ''))
    parser.add_argument('-l', '--log', help='set logging verbosity', type=str,
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        default='warning')
    args = parser.parse_args()
    loader(args.url, args.output, args.log)


if __name__ == '__main__':
    main()
