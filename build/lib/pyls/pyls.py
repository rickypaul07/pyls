import os
import json
from argparse import ArgumentParser
from datetime import datetime


def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def list_directory(contents, show_hidden=False, long_format=False, reverse=False, sort_by_time=False,
                   filter_option=None, human_readable=False):
    if filter_option not in (None, 'file', 'dir'):
        raise ValueError(f"Invalid filter option '{filter_option}'. Available filters are 'file' and 'dir'.")

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


def format_long_listing(item, human_readable=False):
    permissions = item['permissions']
    size = human_readable_size(item['size']) if human_readable else item['size']
    time_modified = datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
    return f"{permissions} {size} {time_modified} {item['name']}"


def human_readable_size(size):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if size < 1024:
            return f"{size:.1f}{unit}" if unit else f"{size}{unit}"
        size /= 1024
    return f"{size:.1f}P"


def main():
    parser = ArgumentParser(description="Python implementation of ls command")
    parser.add_argument('-A', '--all', action='store_true', help="do not ignore entries starting with .")
    parser.add_argument('-l', '--long', action='store_true', help="use a long listing format")
    parser.add_argument('-r', '--reverse', action='store_true', help="reverse order while sorting")
    parser.add_argument('-t', '--time', action='store_true', help="sort by time, newest first")
    parser.add_argument('--filter', choices=['file', 'dir'], help="filter by 'file' or 'dir'")
    parser.add_argument('-H', '--human-readable', action='store_true',
                        help="with -l, print sizes in human readable format")
    parser.add_argument('path', nargs='?', default='structure.json', help="path to the JSON file")
    args = parser.parse_args()

    if not os.path.isfile(args.path):
        print(f"error: cannot access '{args.path}': No such file or directory")
        return

    structure = read_json(args.path)

    if args.path == 'structure.json':
        contents = structure['contents']
    else:
        contents = get_subdirectory_contents(structure, args.path.split('/'))

    if contents is None:
        print(f"error: cannot access '{args.path}': No such file or directory")
    else:
        list_directory(contents, show_hidden=args.all, long_format=args.long, reverse=args.reverse,
                       sort_by_time=args.time, filter_option=args.filter, human_readable=args.human_readable)


def get_subdirectory_contents(structure, path_parts):
    if not path_parts:
        return structure['contents']
    for item in structure['contents']:
        if item['name'] == path_parts[0]:
            if 'contents' in item:
                return get_subdirectory_contents(item, path_parts[1:])
            else:
                return [item] if not path_parts[1:] else None
    return None


if __name__ == '__main__':
    main()
