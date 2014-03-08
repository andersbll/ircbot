# coding: utf-8

import time
import logging

from twisted.words.protocols import irc
from twisted.internet import protocol


def time_now():
    return time.asctime(time.localtime(time.time()))


class IRCBot(irc.IRCClient, protocol.ClientFactory):
    def __init__(self, channel, nickname):
        self.nickname = nickname
        self.channel = channel

    def buildProtocol(self, addr):
        return self

    def clientConnectionLost(self, connector, reason):
        logging.debug('Connection lost: %s' % reason)
        logging.debug('Reconnecting ...')
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logging.debug('Connection failed: %s' % reason)
        logging.debug('Reconnecting ...')
        connector.connect()

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        logging.debug('Signed on to IRC server.')
        self.join(self.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        logging.debug('Has joined channel %s.' % channel)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        user = user.split('!', 1)[0]

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            logging.info('Private message from %s: %s.' % (user, msg))
        else:
            logging.info('Message in %s: %s: %s' % (channel, user, msg))

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            logging.debug("<%s> %s" % (self.nickname, msg))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        logging.debug('* %s %s' % (user, msg))
