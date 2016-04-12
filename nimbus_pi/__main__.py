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


"""The main NimbusPi Weather Station launcher"""

import argparse
import configparser


# Parse any runtime arguments
PARSER = argparse.ArgumentParser(description='The NimbusPi weather station.')

PARSER.add_argument('-c', '--config', default='nimbus.cfg',
                    help="configuration file (default: nimbus.cfg)")

PARSER.add_argument('-q', '--quiet', action='store_true',
                    help='prevents output to stdout')

PARSER.add_argument('-v', '--verbose', action='count', default=0,
                    help='verbosity level for logging (-vv for max verbosity)')

ARGS = PARSER.parse_args()


# Load the NimbusPi configuration
CONFIG = configparser.ConfigParser()

CONFIG.read(ARGS.config)
