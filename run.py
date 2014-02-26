#!/usr/bin/env python3
# coding: utf-8

import sys
import logging
import signal
import argparse
from ircbot import IRCBot


def parse_args():
    description = 'IRC bot'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--server', type=str, default='chat.freenode.org',
                        help='Server address.')
    parser.add_argument('-P', '--port', type=str, default=6667,
                        help='Server port.')
    parser.add_argument('-c', '--channel', type=str, required=True,
                        help='Channel to join.')
    parser.add_argument('-n', '--nick', type=str, required=True,
                        help='Bot nickname.')
    parser.add_argument('-p', '--password', type=str,
                        help='Bot password.')
    parser.add_argument('-v', '--verbosity', type=str,
                        choices=['errors', 'bot', 'debug', 'dump'],
                        default='bot', help='Verbosity level.')
    return parser.parse_args()


def run():
    args = parse_args()
    verbosity_levels = {
        'errors': logging.WARNING,
        'bot': logging.INFO,
        'debug': logging.DEBUG,
        'dump': logging.NOTSET,
    }
    logging.basicConfig(level=verbosity_levels[args.verbosity])
    retval = -1
    while retval != 0:
        bot = IRCBot(args.server, args.port, args.channel, args.nick)

        def handler(signum=None, frame=None):
            bot.disconnect('Process shutdown.')
            sys.exit(0)
        for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGQUIT]:
            signal.signal(sig, handler)

        try:
            retval = bot.start()
        except Exception as e:
            logging.exception('Exception occurred, restarting.')
            if retval != 0 and bot.connection.is_connected():
                bot.disconnect('Exception occurred, restarting.')


if __name__ == '__main__':
    run()
