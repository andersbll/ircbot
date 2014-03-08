#!/usr/bin/env python
# coding: utf-8

import logging
import argparse
from ircbot import IRCBot
from twisted.internet import reactor


def parse_args():
    description = 'IRC bot'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--server', default='chat.freenode.org',
                        help='Server address.')
    parser.add_argument('-P', '--port', type=int, default=6667,
                        help='Server port.')
    parser.add_argument('-c', '--channel', required=True,
                        help='Channel to join.')
    parser.add_argument('-n', '--nick', required=True, help='Bot nickname.')
    parser.add_argument('-p', '--password', help='Bot password.')
    parser.add_argument('-v', '--verbosity',
                        choices=['error', 'bot', 'debug', 'dump'],
                        default='bot', help='Verbosity level.')
    return parser.parse_args()


def run():
    args = parse_args()
    verbosity_levels = {
        'error': logging.WARNING,
        'bot': logging.INFO,
        'debug': logging.DEBUG,
        'dump': logging.NOTSET,
    }
    logging.basicConfig(
        level=verbosity_levels[args.verbosity],
        format='%(levelname)-8s %(message)s',
    )

    bot = IRCBot(args.channel, args.nick)
    reactor.connectTCP(args.server, args.port, bot)
    reactor.run()


if __name__ == '__main__':
    run()
