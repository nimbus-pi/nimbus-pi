# NimbusPi
#
# Copyright 2016 Andrew Vaughan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Launcher for NimbusPI"""


import argparse
import logging
import os
import sys
import traceback

from nimbuspi import NimbusPI



def main(args):
    """Launches the NimbusPI service"""
    
    # Setup global logging parameters
    logger = logging.getLogger()
    
    logger.setLevel(logging.WARNING)
    
    if hasattr(args, 'verbose'):
        if args.verbose == 1:
            logger.setLevel(logging.INFO)
            
        elif args.verbose == 2:
            logger.setLevel(logging.DEBUG)
            logging.getLogger('yapsy').setLevel(logging.INFO)
            
        elif args.verbose > 2:
            logger.setLevel(1)
    
        
    # Setup console logging
    ch_stdout = logging.StreamHandler(sys.stdout)

    ch_stdout.setFormatter(
        logging.Formatter(
            fmt='%(name)-12s :: %(levelname)-8s : %(message)s'
        )
    )

    if args.quiet:
        sys.stdout = os.devnull
        ch_stdout.setLevel(9999)

    logger.addHandler(ch_stdout)
    
    
    # Setup file logging
    if args.log != None:
        fh_log = logging.FileHandler(args.log)

        fh_log.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s] %(name)-12s :: %(levelname)-8s : %(message)s',
                datefmt='%m-%d-%Y %H:%M:%S'
            )
        )

        logger.addHandler(fh_log)
    
    
    # Send all exceptions through the logger
    def handle_exception(ex_cls, ex, trace):
        """Catches all errors and sends them through the logger"""

        logger.critical("EXCEPTION")
        logger.critical(''.join(traceback.format_tb(trace)))
        logger.critical('%s: %s', ex_cls, ex)

    sys.excepthook = handle_exception
    
    
    # Start NimbusPi
    log = logging.getLogger('controller')
    
    log.debug("Launching NimbusPI")
    
    nimbus = NimbusPI(config=args.config)
    nimbus.run()
    
    log.debug("Exiting")



if __name__ == "__main__":
    
    # Setup runtime arguments
    PARSER = argparse.ArgumentParser(prog="nimbus", description='NimbusPi: the modular, open-source weather station.')
    
    PARSER.add_argument('-c', '--config', default='nimbus.cfg',
                        help="configuration file (default: nimbus.cfg)")
                        
    PARSER.add_argument('-q', '--quiet', action='store_true',
                        help='prevents output to stdout')
                        
    PARSER.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level for logging (-vv for max verbosity)')
                        
    PARSER.add_argument('-l', '--log',
                        help='the log file to write to')
    
    
    # Run our main class
    main(PARSER.parse_args())
