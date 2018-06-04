#! /usr/bin/env python3

from collections import defaultdict
import copy
import math
import re
import time

INTERVAL_STATS = 10

RE_COMMON_LOG = re.compile(r'^(?P<client>\S+) - (?P<user_id>\S+) \[(?P<dt>[^\]]+)\] \"(?P<method>[A-Z]+) (?P<request>[\w\/]+) HTTP/[0-9.]+\" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)$')  # noqa


DEFAULT_STATS = {
    'hits_per_page': defaultdict(int),
    'total_hits': 0,
}


def follow(f):
    """
    Generator to follow a file like object
    """
    # Go to the beginning of the file
    f.seek(0)
    while True:
        line = f.readline()
        if not line:
            yield None
        yield line


def parse_log_line(line):
    """
    Parse the log line into useable data
    """
    match = RE_COMMON_LOG.match(line)
    if match:
        return match.groupdict()


def main(filename):
    stats = copy.copy(DEFAULT_STATS)
    with open(filename, 'r') as f:
        for line in follow(f):
            secs = math.floor(time.time())
            printed_stats = secs
            # Print stats every INTERVAL_STATS and only if we haven't printed them before
            if secs % INTERVAL_STATS == 0 and printed_stats == math.floor(time.time()):
                print(stats)

                # Reset the stats
                stats = copy.copy(DEFAULT_STATS)

            # Collect some stats
            if line:
                data = parse_log_line(line.strip())
                if data:
                    stats['total_hits'] += 1
                    page = data['request']
                    stats['hits_per_page'][page] += 1
            else:
                time.sleep(1)


if __name__ == "__main__":
    try:
        filename = 'access.log'
        main('access.log')
    except KeyboardInterrupt:
        pass
