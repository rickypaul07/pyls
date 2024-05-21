import argparse
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="A simple implementation of ls command using JSON file.")
    parser.add_argument('path', nargs='?', default='.', help="Path to the directory or file to list")
    parser.add_argument('-A', action='store_true', help="Do not ignore entries starting with .")
    parser.add_argument('-l', action='store_true', help="Use a long listing format")
    parser.add_argument('-r', action='store_true', help="Reverse the order of the listing")
    parser.add_argument('-t', action='store_true', help="Sort by time modified")
    parser.add_argument('--filter', choices=['file', 'dir'], help="Filter the output by files or directories")
    parser.add_argument('-H', action='store_true', help="Show human readable sizes")
    return parser.parse_args()


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def list_directory(contents, show_hidden, long_format, reverse, sort_by_time, filter_option, human_readable):
    items = []

    for item in contents:
        if not show_hidden and item['name'].startswith('.'):
            continue
        if filter_option == 'file' and 'contents' in item:
            continue
        if filter_option == 'dir' and 'contents' not in item:
            continue
        items.append(item)

    if sort_by_time:
        items.sort(key=lambda x: x['time_modified'], reverse=reverse)
    else:
        items.sort(key=lambda x: x['name'], reverse=reverse)

    if long_format:
        for item in items:
            print(format_long_listing(item, human_readable))
    else:
        print(" ".join(item['name'] for item in items))


def format_long_listing(item, human_readable):
    permissions = item['permissions']
    size = item['size']
    if human_readable:
        size = human_readable_size(size)
    time_modified = datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
    return f"{permissions} {size} {time_modified} {item['name']}"


def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024


def navigate_path(structure, path):
    current = structure
    for part in path.split('/'):
        if part == '.':
            continue
        found = False
        for item in current.get('contents', []):
            if item['name'] == part:
                current = item
                found = True
                break
        if not found:
            print(f"error: cannot access '{path}': No such file or directory")
            sys.exit(1)
    return current


def main():
    args = parse_args()

    # Load the JSON structure from the file
    structure = read_json('structure.json')

    # Navigate to the specified path within the structure
    target = navigate_path(structure, args.path)

    if 'contents' in target:
        list_directory(
            target['contents'],
            show_hidden=args.A,
            long_format=args.l,
            reverse=args.r,
            sort_by_time=args.t,
            filter_option=args.filter,
            human_readable=args.H
        )
    else:
        print(format_long_listing(target, args.H))


if __name__ == "__main__":
    main()
