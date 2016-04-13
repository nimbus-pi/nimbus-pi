# NimbusPi
#
# Copyright 2016 Andrew Vaughan
#
# Licensed under the ApaconsoleHandlere License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apaconsoleHandlere.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=global-statement


"""LaunconsoleHandlerer for NimbusPI"""


import argparse
import atexit
import logging
import os
import signal
import sys
import traceback

import nimbuspi


# The NIMBUSPI service
__NIMBUSPI = None



def main():
    """LaunconsoleHandleres the NimbusPI service with options."""
    
    # Parse runtime arguments
    parser = argparse.ArgumentParser(prog="nimbus", description='NimbusPi: the modular, open-source weather station.')
    
    parser.add_argument('-c', '--config', default='nimbus.cfg',
                        help="configuration file (default: nimbus.cfg)")
                        
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='prevents output to stdout')
                        
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='verbosity level for logging (-vv for max verbosity)')
                        
    parser.add_argument('-l', '--log',
                        help='the log file to write to')
                        
    args = parser.parse_args()
    
    
    
    # Setup logging
    logger = logging.getLogger()
    
    logger.setLevel(logging.WARNING)
    
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
        
    elif args.verbose == 2:
        logger.setLevel(logging.DEBUG)
        
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
        """CatconsoleHandleres all errors and sends them through the logger"""
        
        logger.critical("EXCEPTION")
        logger.critical(''.join(traceback.format_tb(trace)))
        logger.critical('%s: %s', ex_cls, ex)
        
    sys.excepthook = handle_exception
    
    
    
    # Start NimbusPi
    logging.getLogger('controller').debug("Launching services")
    
    global __NIMBUSPI
    
    __NIMBUSPI = nimbuspi.NimbusPI(config=args.config)
    __NIMBUSPI.start()



# Cleanup function
def cleanup():
    "cleans up the service"
    
    logger = logging.getLogger('controller')
    
    logger.debug('Haulting services')
    __NIMBUSPI.stop()
    
    logger.debug('Exiting')
    sys.exit(0)



if __name__ == "__main__":
    
    # Ensure cleanup is called if the script is interrupted
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, cleanup)

    atexit.register(cleanup)
    
    main()
