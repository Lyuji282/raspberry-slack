#!/usr/bin/env python

"""Slack_test.py: Slack bot to control a webcam and post snapshots to Slack ."""


__licence__ = "MIT"
__version__ = "1.0.1"

#date last modified: 17/5/2017

import time
import sys

from slackclient import SlackClient
import psutil

import config
import utils
import lexicon as lx
import SlackBot

# logging module

logger = utils.loggerMaster('slack', logLevel="DEBUG")

from utils import get_temp as temp

#add directory for author testing

sys.path.append('./testing/')

# get authentication details from config file

if len(sys.argv)>1:

    if  sys.argv[1]=='dev':
        logger.info('dev mode')
        location='./testing/dev_config.conf'
    else: location='slack_config.conf'

else:
     location='slack_config.conf'

config_file=config.read_config(str(location))

# signal handler for kill commands

utils.set_signal()

#main loop

if __name__ == ('__main__'):

    bot = SlackBot.SlackBot(config_file)
    bot.generate_client()

    try:

        while True:

            if bot.test_connection(verbose=False):
                bot.process()
                time.sleep(1)
            else:
                pass

    except KeyboardInterrupt:

        logger.warning("Script terminated by user")
        sys.exit(0)

    except ValueError:

        logger.error("Main loop value error, exiting at " +
                     str(bot.run_time) + " seconds.")
        sys.exit(1)

    except Exception as exe:

        logger.exception("Main loop other exception " + str(exe))
        sys.exit(1)
