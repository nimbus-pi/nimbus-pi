# ![nimbus-pi](https://s3.amazonaws.com/f.cl.ly/items/2j0K2G381G333B1K2B3v/banner.png?v=de6bc299)

[![Version][version-image]][version-url]
[![License][license-image]][license-url]
[![Build Status][build-image]][build-url]


NimbusPi is a Raspberry Pi based weather station.  It is intended to be modular and extensible, working with custom
components as well as more-popular weather systems.


# Installation

NimbusPI comes with a Makefile for convenience.  NimbusPI was built on [Python 2.7](https://www.python.org/downloads/)
and is the recommended version for your platform.  You can check your python version by entering the following in the
terminal:

```bash
$ python --version
```

If Python is not installed on your system, you can find instructions for installing it
[on the Python website](https://wiki.python.org/moin/BeginnersGuide/Download).

Once installed, the Makefile will install all required dependencies for you:

```bash
$ sudo make install
```

You can ensure your NimbusPI is installed correctly by running the provided test scripts:

```bash
$ make test
```


# Usage

Once installed, running your NimbusPI is as simple as running the provided executable:

```bash
$ ./nimbus
```

You can find more options for running the NimbusPI service by using the `-h` argument:

```bash
$ ./nimbus -h
```


# Configuration

NimbusPI can run without a configuration file, but it will not do much on its own.  NimbusPI is made to be
configurable!  By default, NimbusPI will look for a `nimbus.cfg` file in your running folder, but you can also specify
a different configuration file by using the `-c` option:

```bash
./nimbus -c /path/to/my/nimbus.cfg
```

The configuration file follows a standard INI format with three sections:

```ini
[station]
name      = My NimbusPI Weather Station
location  = 1234 Test Location, Chicago, IL 60606
latitude  = 1.111111
longitude = -2.222222
altitude  = 8000  # In Feet


[sensors]
mysensor1
mysensor2


[broadcasters]
mybroadcaster1
mybroadcaster2
```

The `station` section is used to describe details about your station.  Some sensors you install can override these
settings, but the config provides a fallback in case the sensors are not available, or do not function.

The `sensors` and `broadcasters` sections contain lists of plugins to activate when the NimbusPI weather station is
started.

Sensor and Broadcaster plugins may also have configuration settings that should also be included in your root
configuration file.  Please refer to your plugin's instructions for what configuration options are available for each
module you wish to install.


# Contributing

There are many ways to contribute to NimbusPI!  If you have an idea, or have discovered a bug, please
[open an issue](https://github.com/nimbus-pi/nimbus-pi/issues) so it can be addressed.

If you are interested in contributing to the project through design or development, please read our
[Contribution Guidelines](https://github.com/nimbus-pi/nimbus-pi/blob/master/CONTRIBUTING.md).


# Release Policy

Releases of NimbusPi follow [Semantic Versioning](http://semver.org/) standards in a `MAJOR.MINOR.PATCH` versioning
scheme of the following format:

* `MAJOR` - modified when major, incompatible changes are made to the application,
* `MINOR` - modified when functionality is added in a backwards-compatible manner, and
* `PATCH` - patches to existing functionality, such as documentation and bug fixes.


# License

```
Copyright 2016 Andrew Vaughan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```



[version-image]: http://img.shields.io/badge/release-0.0.0-blue.svg?style=flat
[version-url]:   https://github.com/nimbus-pi/nimbus-pi/releases
[license-image]: http://img.shields.io/badge/license-Apache_2.0-blue.svg?style=flat
[license-url]:   https://github.com/nimbus-pi/nimbus-pi/blob/master/LICENSE
[build-image]:   https://travis-ci.org/nimbus-pi/nimbus-pi.svg?branch=master
[build-url]:     https://travis-ci.org/nimbus-pi/nimbus-pi
