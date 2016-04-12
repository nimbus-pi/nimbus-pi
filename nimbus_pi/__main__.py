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
import logging
import os
import sys
import traceback

import configparser

from yapsy.PluginManager import PluginManager

import nimbus_pi.plugins as plugins


# The current version
VERSION = "0.1.0-rc1"



# Parse any runtime arguments
PARSER = argparse.ArgumentParser(description='The NimbusPi weather station.')

PARSER.add_argument('-c', '--config', default='nimbus.cfg',
                    help="configuration file (default: nimbus.cfg)")

PARSER.add_argument('-q', '--quiet', action='store_true',
                    help='prevents output to stdout')

PARSER.add_argument('-v', '--verbose', action='count', default=0,
                    help='verbosity level for logging (-vv for max verbosity)')

ARGS = PARSER.parse_args()



# Add a verbose call to the logging controls
logging.addLevelName(5, "VERBOSE")

def verbose_logging(self, message, *args):
    """Adds verbose logging support to the Python logger."""
    if self.isEnabledFor(5):
        self.log(5, message, *args)

logging.Logger.verbose = verbose_logging



# Initialize the logger
LOGGER = logging.getLogger('nimbuspi')
LOGGER_YAPSY = logging.getLogger('yapsy')

if ARGS.verbose == 1:
    LOGGER.setLevel(logging.DEBUG)
    LOGGER_YAPSY.setLevel(logging.INFO)
elif ARGS.verbose > 1:
    LOGGER.setLevel(1)
    LOGGER_YAPSY.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)
    LOGGER_YAPSY.setLevel(logging.INFO)



# Send all exceptions through the logger
def handle_exception(ex_cls, ex, trace):
    """catches all errors and sends them through the logger"""

    LOGGER.critical("EXCEPTION")
    LOGGER.critical(''.join(traceback.format_tb(trace)))
    LOGGER.critical('%s: %s', ex_cls, ex)

sys.excepthook = handle_exception



# Setup console logging
CH = logging.StreamHandler(sys.stdout)

CH.setFormatter(
    logging.Formatter(
        fmt='%(name)-12s : %(levelname)-8s : %(message)s'
    )
)

if ARGS.quiet:
    sys.stdout = os.devnull
    CH.setLevel(9999)

LOGGER.addHandler(CH)
LOGGER_YAPSY.addHandler(CH)



# Start NimbusPi
LOGGER.info("NimbusPi Weather Station v%s", VERSION)
LOGGER.info("-" * 80)

LOGGER.debug("Invoked with options:")
LOGGER.debug(ARGS)

LOGGER.debug("Logging level: %d", LOGGER.getEffectiveLevel())



# Load the NimbusPi configuration
CONFIG = configparser.ConfigParser(allow_no_value=True)

LOGGER.info("Loading configuration...")

LOGGER.debug("Loading config file '%s'", ARGS.config)
CONFIG.read(ARGS.config)

for section in CONFIG.sections():
    for option in CONFIG.options(section):
        LOGGER.verbose("Config :: %s.%s = %s", section, option, CONFIG.get(section, option))



# Load the plugins
LOGGER.debug("Searching for plugins...")

PLUGINS = PluginManager(plugin_info_ext='info')

PLUGINS.setPluginPlaces([
    './sensors',
    './broadcasters',
    './nimbus_pi/sensors',
    './nimbus_pi/broadcasters'
])

PLUGINS.setCategoriesFilter({
    plugins.ISensorPlugin.CATEGORY      : plugins.ISensorPlugin,
    plugins.IBroadcasterPlugin.CATEGORY : plugins.IBroadcasterPlugin
})

PLUGINS.collectPlugins()

for plugin in PLUGINS.getAllPlugins():
    LOGGER.verbose("Plugin loaded: %s (%s)", plugin.name, plugin.path)

LOGGER.debug("%d plugins available", len(PLUGINS.getAllPlugins()))



# Load the sensor plugins
LOGGER.debug("Activating sensor plugins...")

SENSORS = {}

if not CONFIG.has_section('sensors'):
    LOGGER.error("Sensors section missing from configuration.")
    sys.exit(1)

for sensor in CONFIG.options('sensors'):
    LOGGER.verbose("Activating sensor '%s'", sensor)

    PLUGINS.activatePluginByName(sensor, category=plugins.ISensorPlugin.CATEGORY)
    plugin = PLUGINS.getPluginByName(sensor, category=plugins.ISensorPlugin.CATEGORY)

    SENSORS[sensor] = plugin.plugin_object




# # Load the broadcaster plugins
# LOGGER.debug("Activating broadcaster plugins...")
# # TODO
